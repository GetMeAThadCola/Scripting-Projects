# AWS Security Audit Script

🚀 **A single-file Python tool to audit AWS accounts for security misconfigurations.**

Cloud security misconfigurations are among the biggest causes of data breaches. This Python script scans an AWS environment and highlights potential security risks across IAM, S3, EC2, networking, and logging configurations—all with color-coded output and JSON reporting.

---

## ✨ Features

✅ **Single-file simplicity**
- No complex modules
- Easy to run and share

✅ **Color-coded console output**
- 🟢 Green → Good
- 🟠 Orange → Medium risk
- 🔴 Red → Critical issue
- 🟣 Purple → No resources found

✅ **Security Checks Included**
- IAM Users
  - Users without MFA
  - Old or unused access keys
  - Users with no policies
  - AdministratorAccess attached directly
- IAM Roles
  - Roles trusted by external accounts
- IAM Policies
  - Policies containing wildcards (`*`)
- S3 Buckets
  - Publicly accessible buckets
  - Buckets without encryption
  - Missing versioning or logging
- EC2 & Networking
  - Security Groups open to 0.0.0.0/0
  - Default VPC detection
- Logging & Monitoring
  - CloudTrail enabled and validated
  - GuardDuty enabled
- Cost/Exposure
  - Idle resources checks (future enhancement)

✅ **JSON Report Export**
- Save all findings to a structured JSON file for further analysis

---

## 🛠️ Requirements

- Python 3.x
- Boto3
- Colorama

Install requirements:

```bash
pip install -r requirements.txt

🔎 How to Run
Configure AWS CLI credentials if not already set:

bash
Copy
Edit
aws configure
Run the audit script:

bash
Copy
Edit
python aws_audit.py
Find your report:

A JSON file audit_report.json will be created in the same directory.

🔗 Connect
I’m always open to feedback or collaboration! Feel free to connect with me on LinkedIn. www.linkedin.com/in/huntertcarbone

#CyberSecurity #CloudSecurity #AWS #Python #DevSecOps