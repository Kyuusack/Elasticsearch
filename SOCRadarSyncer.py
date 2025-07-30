import os
import json
import requests
import logging
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth

# Configuration variables
elasticsearch_host = "https://elasticsearch:9200"
elastic_user = "elastic"
elastic_password = "YOUR_PASSWORD_ELASTIC"
index_pattern = ".internal.alerts-security.alerts-default-*" // Indeks pattern refer to Security Alerts
timestamp_field = "@timestamp"
query_interval_hours = 6  # Query interval in hours (6 hours)

# SOCRadar API endpoint and secret
socradar_api_key = "YOUR_SOCRADAR_API"
socradar_fp_url = "https://platform.socradar.com/api/company/YOUR_COMPANY_ID/incidents/fp"
socradar_resolve_url = "https://platform.socradar.com/api/company/YOUR_COMPANY_ID/incidents/resolve"

# Disable SSL verification if needed (for self-signed certs)
requests.packages.urllib3.disable_warnings()

# Logging setup
log_path = "/var/log/external/socradar-syncer/sync.log" // Log path for debugging
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def query_elasticsearch():
    """Queries Elasticsearch for documents in the last 6 hours with specific filter conditions."""
    url = f"{elasticsearch_host}/{index_pattern}/_search"

    # Set the time range filter for the last 6 hours
    six_hours_ago = (datetime.utcnow() - timedelta(hours=query_interval_hours)).strftime('%Y-%m-%dT%H:%M:%S')

    # Query body
    query_body = {
        "query": {
            "bool": {
                "must": [
                    { "match": { "kibana.alert.status": "active" } },
                    { "match": { "kibana.alert.workflow_status": "closed" } },
                    { "terms": { "kibana.alert.workflow_tags": ["Valid Threat", "False Positive"] } },
                    { "match": { "event.dataset": "socradar" } }
                ],
                "filter": {
                    "range": {
                        timestamp_field: {
                            "gte": six_hours_ago,
                            "lte": "now"
                        }
                    }
                }
            }
        },
        "_source": ["kibana.alert.workflow_tags", "kibana.alert.status", "kibana.alert.workflow_status", "event.category", "event.action", "@timestamp", "logtype", "alarm_id", "kibana.alert.workflow_user"]
    }

    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(query_body),
        auth=HTTPBasicAuth(elastic_user, elastic_password),
        verify=False  # Skips SSL verification for self-signed certs
    )

    if response.status_code == 200:
        result = response.json()
        hits = result.get("hits", {}).get("hits", [])
        return hits
    else:
        logging.error(f"Error querying Elasticsearch: {response.text}")
        return []

def send_to_socradar(alert, action_type):
    """Sends the update to SOCRadar based on the workflow tag."""
    alarm_id = alert['_source']['alarm_id']
    workflow_user = alert['_source']['kibana.alert.workflow_user']

    if action_type == "False Positive":
        # False Positive - update via 'fp' endpoint
        url = socradar_fp_url
    elif action_type == "Valid Threat":
        # Valid Threat - update via 'resolve' endpoint
        url = socradar_resolve_url
    else:
        return  # No action for other tags

    data = {
        "comments": f"SOCRadar syncer closed by {workflow_user}",
        "notification_ids": [alarm_id]
    }

    headers = {
        'Api-Key': socradar_api_key,
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

    if response.status_code == 200:
        logging.info(f"Notification id {alarm_id} {alert['_source']['event.action']} was tagged as {action_type} by {workflow_user}")
    else:
        logging.error(f"Failed to update SOCRadar for alert {alarm_id}: {response.text}")

def main():
    # Step 1: Query Elasticsearch for new documents in the last 6 hours
    alerts = query_elasticsearch()

    # Step 2: If new documents are found, process them
    if alerts:
        for alert in alerts:
            workflow_tags = alert['_source'].get('kibana.alert.workflow_tags', [])
            if workflow_tags:
                for tag in workflow_tags:
                    if tag == "False Positive" or tag == "Valid Threat":
                        send_to_socradar(alert, tag)
    else:
        logging.info("No new alerts to process.")

if __name__ == "__main__":
    main()
