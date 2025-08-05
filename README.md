
---

# 🔐 XSOAR IP Range Uploader

This Python script automates the process of adding **IP address ranges (CIDR)** to a **Cortex XSOAR investigation** using the `!checkpoint-address-range-add` command. It's especially useful for SOC or Blue Team operations dealing with threat intelligence or malicious IPs from external alerts.

---

## 📁 Project Structure

```
.
├── ip_ranges.txt         # List of CIDR ranges (one per line)
├── script.py             # Main Python script
└── README.md             # Documentation (this file)
```

---

## ⚙️ Features

* Reads a list of CIDR ranges from a text file.
* Calculates the first and last usable IP from each range.
* Sends a POST request to the XSOAR API with the appropriate command.
* Takes input for Cookies, Investigation ID, and Session ID.
* Loops through multiple IP ranges automatically.

---

## 🧾 ip\_ranges.txt Format

Each line should contain a valid CIDR block, e.g.:

```
192.168.1.0/24
10.10.10.0/28
203.0.113.0/29
```

---

## 💻 How to Use

1. Create or update `ip_ranges.txt` with the list of CIDRs.
2. Run the script:

   ```bash
   python3 script.py
   ```
3. Provide the required input when prompted:

   * Your XSOAR session **Cookies**
   * The **Investigation ID**
   * The **Session ID** from your Checkpoint system

---

## ✅ Sample Output

```bash
Input Your Cookies: D1SESSIONID=abcd1234...
Input Investigation ID: 12345
Input Session ID: CP1234567890

Processing IP range: 192.168.1.0/24
Success adding IP range 192.168.1.0/24

Processing IP range: 10.10.10.0/28
Success adding IP range 10.10.10.0/28
```

---

## 🔐 Security Notes

* Only use this script in secure and authorized environments.
* Never commit cookies, session IDs, or sensitive data to a public repository.
* For production use, remove `verify=False` from the `requests.post()` call and use a valid SSL certificate.

---

## 🧰 Requirements

* Python 3.x
* Libraries:

  * `requests`
  * `ipaddress` (standard library, no installation needed)

You can install `requests` via:

```bash
pip install requests
```

---

## 📜 License

MIT License — feel free to use, modify, and share with proper credit.

---
