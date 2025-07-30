🔁 Elastic SIEM x SOCRadar Syncer
# Learning Scripts for Elastic SIEM Enterprise 🚀
This repository is your go-to resource for automating incident syncs between Elastic SIEM Enterprise and SOCRadar. 🧠
Built for SIEM Engineers by a SIEM Engineer, this tool bridges the gap between alerting and external incident management—empowering you to act faster and smarter. 💪
📌 What This Script Does

This Python script automates the process of identifying specific security alerts from Elastic SIEM (such as false positives or valid threats) and pushing updates to SOCRadar's Incident Platform via API.

You can use it to:

    ✅ Automatically scan and filter alerts from Elastic SIEM every 6 hours

    🔄 Sync alerts marked with workflow tags like "False Positive" or "Valid Threat" to SOCRadar

    🧾 Generate logs for every successful or failed sync attempt

    🧪 Test or integrate workflows between SOAR/SIEM and external threat platforms

⚙️ How It Works

    Connects to Elasticsearch:
    Queries .internal.alerts-security.alerts-default-* indices for alerts from the last 6 hours, filtering by:

        kibana.alert.status: active

        kibana.alert.workflow_status: closed

        kibana.alert.workflow_tags: either "Valid Threat" or "False Positive"

        event.dataset: socradar

    Processes Matching Alerts:
    Extracts each relevant alert and reads its tag and metadata.

    Syncs with SOCRadar:

        Alerts tagged False Positive → sent to SOCRadar’s /fp endpoint

        Alerts tagged Valid Threat → sent to SOCRadar’s /resolve endpoint

    Logs All Activity:
    Sync results are logged to /var/log/external/socradar-syncer/sync.log.

🛠️ Requirements

    Python 3.x

    requests library

Install dependencies:

pip install requests

🧰 Configuration

Update the following variables in the script:

elasticsearch_host = "https://elasticsearch:9200"
elastic_user = "elastic"
elastic_password = "YOUR_PASSWORD_ELASTIC"

socradar_api_key = "YOUR_SOCRADAR_API"
socradar_fp_url = "https://platform.socradar.com/api/company/YOUR_COMPANY_ID/incidents/fp"
socradar_resolve_url = "https://platform.socradar.com/api/company/YOUR_COMPANY_ID/incidents/resolve"

    🔐 Pro Tip: Use environment variables or a secrets manager to store credentials securely.

🧪 Example Use Case

You close an alert in Kibana and mark it as "False Positive" or "Valid Threat".
Within the next 6-hour scan window, this script detects the tag and pushes the alert status to SOCRadar’s incident system automatically. No manual updates needed.
🚀 Run the Script

python socradar_sync.py

Or set up as a cronjob to run every 6 hours:

0 */6 * * * /usr/bin/python3 /path/to/socradar_sync.py

📄 Log Output Example

2025-07-30 12:03:01 - Notification id 7832743 socradar_threat was tagged as False Positive by analyst_joe

🛡️ Who This Is For

This script is ideal for:

    SOC teams running Elastic SIEM Enterprise

    Engineers integrating Elastic SIEM with external threat intelligence platforms

    Anyone automating detection → triage → response flows

💡 Tip

Want to customize detection logic or sync intervals?
Just tweak the query_body or the query_interval_hours variable.
🤝 Contributing

Found a bug or want to improve the logic? PRs welcome!
Feel free to fork and adapt for your environment.
🧠 Stay Sharp, Stay Safe!

I hope this script becomes a valuable part of your SIEM automation toolkit.
Let’s keep building powerful, efficient, and secure detection ecosystems. 🌐🛠️
