HIPAA Audit & AWS Security Compliance Checker
Overview
This Python-based audit tool evaluates AWS environments and administrative practices against key HIPAA security safeguards. It provides a color-coded report with severity ratings, current status, and actionable remediation steps.

Key Features

✅ AWS environment scan using boto3

✅ Checks for CloudTrail, GuardDuty, Macie, Config, S3 encryption & public access

✅ Administrative safeguard questionnaire (YAML-based)

✅ CLI tool with tabulated, color-coded output

✅ Actionable remediation suggestions for each failed check

Skills Demonstrated

AWS Security & Governance (IAM, S3, Config, GuardDuty, Macie, CloudTrail)

Python Automation with boto3

CLI Tool Design & User Input Handling

YAML-based configuration parsing

Security Compliance Reporting

Usage

bash
Copy
Edit
# Install dependencies
pip install -r requirements.txt

# Run administrative safeguards questionnaire
python hipaa_audit.py questionnaire --file hipaa_checklist.yml

# Run AWS environment scan
python hipaa_audit.py aws --profile my-aws-profile --region us-west-2
Disclaimer
This is a demonstration tool for educational purposes only. It does not constitute legal advice.