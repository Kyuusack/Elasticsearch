# 🚨 Close Alarm Script for Event-of-Interest Alerts 🚨#
This script is designed to automatically close alarms in Elasticsearch that are tagged as "event-of-interest". The alarms that are open and match the specified query will be updated to closed, helping streamline incident management.

🔍 How it works:
- The script leverages the Elasticsearch _update_by_query API to:
- Filter open alarms (kibana.alert.workflow_status = "open").
- Match alarms tagged with "event-of-interest" (kibana.alert.rule.tags).
- Once alarms are matched, their workflow_status and status fields are updated to "closed", effectively resolving the alarm automatically.

✨ Features:
- Auto-close alarms that are tagged as "event-of-interest".
- Efficient querying to find specific alarms based on status and tags.
- Easily customizable for different alarm statuses or tags.

📜 Usage:
- Replace credentials: Edit the script to include your Elasticsearch username and password.
- Run the script: Execute it to automatically close the alarms of interest.

🔧 Dependencies:
- Requires curl and access to your Elasticsearch cluster.
- Elasticsearch version supporting _update_by_query API.
  
🔗 References:
- Elasticsearch Update by Query API - https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update-by-query.html
- Painless Scripting Language - https://www.elastic.co/guide/en/elasticsearch/painless/current/painless-script-index.html
