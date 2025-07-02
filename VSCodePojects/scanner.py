import boto3
import botocore
import json
from datetime import datetime, timezone, timedelta
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

findings = []

def add_finding(severity, category, message, resource=""):
    color = {
        "GOOD": Fore.GREEN,
        "MEDIUM": Fore.YELLOW,
        "BAD": Fore.RED,
        "NONE": Fore.MAGENTA
    }[severity]

    text = f"{color}[{severity}] {category}: {message}"
    if resource:
        text += f" ({resource})"

    print(text)

    # Save finding to report
    findings.append({
        "severity": severity,
        "category": category,
        "message": message,
        "resource": resource
    })

def check_iam_users():
    iam = boto3.client('iam')
    users = iam.list_users()['Users']

    if not users:
        add_finding("NONE", "IAM", "No IAM users found.")
        return

    for user in users:
        username = user['UserName']

        # MFA Check
        mfa = iam.list_mfa_devices(UserName=username)
        if not mfa['MFADevices']:
            add_finding("BAD", "IAM", "User has no MFA enabled.", username)
        else:
            add_finding("GOOD", "IAM", "User has MFA enabled.", username)

        # Access Key Age
        keys = iam.list_access_keys(UserName=username)['AccessKeyMetadata']
        for key in keys:
            create_date = key['CreateDate']
            age_days = (datetime.now(timezone.utc) - create_date).days
            if age_days > 90:
                add_finding("MEDIUM", "IAM", f"Access key is {age_days} days old.", username)

        # Access Key Usage
        for key in keys:
            key_id = key['AccessKeyId']
            last_used = iam.get_access_key_last_used(AccessKeyId=key_id).get('AccessKeyLastUsed', {}).get('LastUsedDate')
            if last_used:
                days_since_use = (datetime.now(timezone.utc) - last_used).days
                if days_since_use > 90:
                    add_finding("MEDIUM", "IAM", f"Access key unused for {days_since_use} days.", username)
            else:
                add_finding("MEDIUM", "IAM", "Access key has never been used.", username)

    # Users with no policies
    for user in users:
        attached = iam.list_attached_user_policies(UserName=user['UserName'])['AttachedPolicies']
        if not attached:
            add_finding("MEDIUM", "IAM", "User has no policies attached.", user['UserName'])

def check_iam_roles():
    iam = boto3.client('iam')
    roles = iam.list_roles()['Roles']

    for role in roles:
        trust_policy = role['AssumeRolePolicyDocument']
        for statement in trust_policy.get('Statement', []):
            principal = statement.get('Principal', {})
            if 'AWS' in principal:
                aws_principal = principal['AWS']
                if isinstance(aws_principal, str) and not aws_principal.startswith("arn:aws:iam::YOUR_ACCOUNT_ID"):
                    add_finding("BAD", "IAM", "Role trusted by external account!", role['RoleName'])

def check_s3_buckets():
    s3 = boto3.client('s3')
    try:
        buckets = s3.list_buckets()['Buckets']
    except Exception as e:
        add_finding("BAD", "S3", f"Could not list buckets: {e}")
        return

    if not buckets:
        add_finding("NONE", "S3", "No S3 buckets found.")
        return

    for bucket in buckets:
        name = bucket['Name']

        # Public Access
        try:
            acl = s3.get_bucket_acl(Bucket=name)
            for grant in acl['Grants']:
                grantee = grant['Grantee']
                if grantee.get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                    add_finding("BAD", "S3", "Bucket is publicly accessible!", name)
        except Exception as e:
            add_finding("BAD", "S3", f"Could not check ACL: {e}", name)

        # Encryption
        try:
            s3.get_bucket_encryption(Bucket=name)
            add_finding("GOOD", "S3", "Bucket has encryption enabled.", name)
        except botocore.exceptions.ClientError as e:
            if "ServerSideEncryptionConfigurationNotFoundError" in str(e):
                add_finding("MEDIUM", "S3", "Bucket has no encryption enabled.", name)

        # Versioning
        versioning = s3.get_bucket_versioning(Bucket=name)
        if versioning.get('Status') != 'Enabled':
            add_finding("MEDIUM", "S3", "Bucket versioning is not enabled.", name)

        # Logging
        logging = s3.get_bucket_logging(Bucket=name)
        if 'LoggingEnabled' not in logging:
            add_finding("MEDIUM", "S3", "Bucket logging is not enabled.", name)

def check_security_groups():
    ec2 = boto3.client('ec2')
    sgs = ec2.describe_security_groups()['SecurityGroups']

    if not sgs:
        add_finding("NONE", "EC2", "No Security Groups found.")
        return

    for sg in sgs:
        sg_id = sg['GroupId']
        for perm in sg.get('IpPermissions', []):
            proto = perm.get('IpProtocol')
            from_port = perm.get('FromPort')
            ip_ranges = perm.get('IpRanges', [])

            for ip_range in ip_ranges:
                cidr = ip_range.get('CidrIp')
                if cidr == '0.0.0.0/0':
                    if proto == '-1':
                        add_finding("BAD", "EC2", "Security Group allows ALL traffic from anywhere.", sg_id)
                    elif from_port in [22, 3389, 80, 443]:
                        add_finding("MEDIUM", "EC2", f"Security Group allows port {from_port} open to the world.", sg_id)

def check_default_vpc():
    ec2 = boto3.client('ec2')
    vpcs = ec2.describe_vpcs()['Vpcs']
    for vpc in vpcs:
        if vpc.get('IsDefault'):
            add_finding("MEDIUM", "VPC", "Default VPC still exists.", vpc['VpcId'])
            return
    add_finding("GOOD", "VPC", "No default VPCs found.")

def check_cloudtrail():
    ct = boto3.client('cloudtrail')
    trails = ct.describe_trails()['trailList']
    if not trails:
        add_finding("BAD", "CloudTrail", "No CloudTrails found!")
        return

    for trail in trails:
        if not trail.get('LogFileValidationEnabled'):
            add_finding("MEDIUM", "CloudTrail", "Log file validation is disabled.", trail['Name'])

def check_guardduty():
    gd = boto3.client('guardduty')
    detectors = gd.list_detectors()['DetectorIds']
    if not detectors:
        add_finding("BAD", "GuardDuty", "GuardDuty is NOT enabled!")
        return
    add_finding("GOOD", "GuardDuty", "GuardDuty is enabled.")

def save_json_report(filename="audit_report.json"):
    with open(filename, "w") as f:
        json.dump(findings, f, indent=2)
    print(f"{Fore.CYAN}Results saved to {filename}")

def run_audit(write_report=False):
    print(Fore.CYAN + "=== STARTING AWS SECURITY AUDIT ===")
    check_iam_users()
    check_iam_roles()
    check_s3_buckets()
    check_security_groups()
    check_default_vpc()
    check_cloudtrail()
    check_guardduty()
    print(Fore.CYAN + "=== AUDIT COMPLETE ===")

    if write_report:
        save_json_report()

if __name__ == "__main__":
    # Run with report saving enabled
    run_audit(write_report=True)
