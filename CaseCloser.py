#!/bin/bash

# URL Elasticsearch _update_by_query endpoint
ES_URL="https://elasticsearch:9200/.internal.alerts-security.alerts-default-*/_update_by_query"

# Basic auth credentials
ES_USER="YOUR_ELASTIC_USERNAME"
ES_PASS="YOUR_ELASTIC_PASSWORD"

# Curl command untuk update workflow_status jadi closed
curl -u "$ES_USER:$ES_PASS" -k -X POST "$ES_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "bool": {
        "must": [
          { "term": { "kibana.alert.workflow_status": "open" }},
          { "match": { "kibana.alert.rule.tags": "event-of-interest" }}
        ]
      }
    },
    "script": {
      "source": "ctx._source[\"kibana.alert.workflow_status\"] = \"closed\"; ctx._source[\"kibana.alert.status\"] = \"closed\";",
      "lang": "painless"
    }
  }'
