import argparse, json, sys, time, traceback
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any, Tuple

# Optional libs (only needed for pretty output)
from tabulate import tabulate
from colorama import Fore, Style
import yaml

# ------------------------- Common structures -------------------------
@dataclass
class Finding:
    control_id: str
    title: str
    severity: str       # "HIGH" | "MEDIUM" | "LOW" | "INFO"
    passed: bool
    details: str
    remediation: str

    def to_row(self):
        sev_color = {
            "HIGH": Fore.RED,
            "MEDIUM": Fore.YELLOW,
            "LOW": Fore.CYAN,
            "INFO": Fore.WHITE,
        }.get(self.severity, Fore.WHITE)
        status = (Fore.GREEN+"PASS"+Style.RESET_ALL) if self.passed else (Fore.RED+"FAIL"+Style.RESET_ALL)
        return [self.control_id, self.title, sev_color+self.severity+Style.RESET_ALL, status, self.details, self.remediation]

def score(findings: List[Finding]) -> Tuple[int,int]:
    total = len([f for f in findings if f.severity in ("HIGH","MEDIUM","LOW")])
    passed = len([f for f in findings if f.passed and f.severity in ("HIGH","MEDIUM","LOW")])
    return passed, total

def print_report(findings: List[Finding], title: str):
    print("\n"+("="*80))
    print(title)
    print("="*80)
    rows = [f.to_row() for f in findings]
    headers = ["Control", "Check", "Severity", "Status", "Details", "Remediation"]
    print(tabulate(rows, headers=headers, tablefmt="grid", maxcolwidths=[10, 28, 9, 8, 40, 40]))
    passed, total = score(findings)
    pct = 0 if total == 0 else int(round((passed/total)*100))
    print(f"\nOverall score: {passed}/{total} ({pct}%)")
    print("(This tool provides guidance only; it is not legal advice.)")

# ------------------------- AWS checks (technical safeguards) -------------------------
def run_aws_checks(profile: str, region: str) -> List[Finding]:
    import boto3
    from botocore.exceptions import ClientError

    session = boto3.Session(profile_name=profile or None, region_name=region or None)
    sts = session.client("sts")
    iam = session.client("iam")
    s3 = session.client("s3")
    s3control = session.client("s3control")
    cloudtrail = session.client("cloudtrail")
    config = session.client("config")
    guardduty = session.client("guardduty")
    macie2 = session.client("macie2")

    findings: List[Finding] = []

    # Helper: safe call wrapper
    def try_call(fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs), None
        except ClientError as e:
            return None, e

    acct = sts.get_caller_identity()["Account"]

    # Root MFA
    summ = iam.get_account_summary()["SummaryMap"]
    root_mfa = summ.get("AccountMFAEnabled", 0) == 1
    findings.append(Finding(
        "TS-1", "Root account MFA enabled", "HIGH", root_mfa,
        "AccountMFAEnabled=1" if root_mfa else "Root MFA disabled",
        "Enable MFA on root in IAM console: IAM → Dashboard → Security recommendations → Activate MFA."
    ))

    # Password policy
    pwd, err = try_call(iam.get_account_password_policy)
    if err:
        findings.append(Finding(
            "AS-PP", "Strong password policy", "MEDIUM", False,
            f"No password policy or access denied: {err.response.get('Error',{}).get('Code')}",
            "Set a strong password policy (min length ≥14, require uppercase/lowercase/number/symbol, max age ≤ 90 days). IAM → Account settings."
        ))
    else:
        pol = pwd["PasswordPolicy"]
        ok = all([
            pol.get("MinimumPasswordLength", 0) >= 14,
            pol.get("RequireSymbols", False),
            pol.get("RequireNumbers", False),
            pol.get("RequireUppercaseCharacters", False),
            pol.get("RequireLowercaseCharacters", False),
        ])
        findings.append(Finding(
            "AS-PP", "Strong password policy", "MEDIUM", ok,
            f"Len={pol.get('MinimumPasswordLength')}, U={pol.get('RequireUppercaseCharacters')}, L={pol.get('RequireLowercaseCharacters')}, N={pol.get('RequireNumbers')}, S={pol.get('RequireSymbols')}",
            "Update IAM password policy to ≥14 chars and require upper/lower/number/symbol. Consider rotation ≤ 90 days."
        ))

    # Account-level S3 public access block
    pab, err = try_call(s3control.get_public_access_block, AccountId=acct)
    pab_ok = False
    if err:
        details = f"No account PublicAccessBlock or access denied"
    else:
        cfg = pab["PublicAccessBlockConfiguration"]
        pab_ok = all(cfg.get(x, False) for x in [
            "BlockPublicAcls", "IgnorePublicAcls", "BlockPublicPolicy", "RestrictPublicBuckets"
        ])
        details = str(cfg)
    findings.append(Finding(
        "TS-2", "S3 account Public Access Block = ON", "HIGH", pab_ok,
        details,
        "S3 console → Block Public Access (account level) → Turn on all four toggles."
    ))

    # CloudTrail trail exists & logging
    trails = cloudtrail.describe_trails()["trailList"]
    ct_ok = False
    ct_details = "No trails"
    if trails:
        # Check if any multi-region trail is logging
        ct_ok = False
        for t in trails:
            status, _ = try_call(cloudtrail.get_trail_status, Name=t["Name"])
            if status and status.get("IsLogging"):
                ct_ok = True
                ct_details = f"Trail {t['Name']} logging"
                break
        if not ct_ok:
            ct_details = "Trail(s) found but not logging"
    findings.append(Finding(
        "TS-3", "CloudTrail logging enabled", "HIGH", ct_ok,
        ct_details,
        "Create a multi-region trail and ensure `IsLogging` is true. CloudTrail → Trails → Create trail."
    ))

    # AWS Config recorder enabled
    recs = config.describe_configuration_recorder_status().get("ConfigurationRecordersStatus", [])
    cfg_ok = any(r.get("recording") for r in recs)
    findings.append(Finding(
        "TS-4", "AWS Config recorder enabled", "HIGH", cfg_ok,
        "Recording ON" if cfg_ok else "No active recorder",
        "AWS Config → Set up recorder with global resource types included."
    ))

    # GuardDuty enabled
    dets = guardduty.list_detectors().get("DetectorIds", [])
    gd_ok = False
    if dets:
        det_id = dets[0]
        det = guardduty.get_detector(DetectorId=det_id)
        gd_ok = det.get("Status") == "ENABLED"
    findings.append(Finding(
        "TS-5", "GuardDuty enabled", "MEDIUM", gd_ok,
        "Enabled" if gd_ok else "Not enabled",
        "Security → GuardDuty → Enable detector for the region."
    ))

    # Macie enabled
    macie, err = try_call(macie2.get_macie_session)
    macie_ok = bool(macie and macie.get("status") == "ENABLED")
    findings.append(Finding(
        "TS-6", "Macie enabled", "LOW", macie_ok,
        "Enabled" if macie_ok else "Disabled",
        "Security → Macie → Enable to discover sensitive data in S3."
    ))

    # S3 bucket defaults: encryption & public
    b_resp = s3.list_buckets()
    buckets = [b["Name"] for b in b_resp.get("Buckets", [])]
    # For brevity, sample up to first 25
    sample = buckets[:25]
    for name in sample:
        # Public?
        is_public = False
        pol, _ = try_call(s3.get_bucket_policy_status, Bucket=name)
        if pol and pol.get("PolicyStatus", {}).get("IsPublic"):
            is_public = True
        # Encryption?
        enc = False
        e, _ = try_call(s3.get_bucket_encryption, Bucket=name)
        if e and e.get("ServerSideEncryptionConfiguration", {}).get("Rules"):
            enc = True

        findings.append(Finding(
            f"S3-{name}",
            f"S3 bucket '{name}' private & encrypted",
            "HIGH" if is_public else "MEDIUM",
            (not is_public) and enc,
            f"public={is_public}, encryption={'ON' if enc else 'OFF'}",
            "Block public access and enable default encryption (SSE-S3 or SSE-KMS) on the bucket."
        ))

    return findings

# ------------------------- Questionnaire checks -------------------------
# A tiny, practical checklist you can expand later.
DEFAULT_QUESTIONNAIRE = """
administrative:
  - id: AS-1
    text: "Privacy & Security Officer assigned"
    weight: 3
    remediation: "Designate a Privacy and a Security Officer and document responsibilities."
  - id: AS-2
    text: "Annual risk analysis performed and documented"
    weight: 5
    remediation: "Perform and document an enterprise risk analysis (45 CFR 164.308(a)(1)(ii)(A))."
  - id: AS-3
    text: "Workforce HIPAA training completed within last 12 months"
    weight: 4
    remediation: "Provide training and maintain records; retrain annually and on policy changes."

physical:
  - id: PS-1
    text: "Facility entry controls defined (badges/visitors/logs)"
    weight: 2
    remediation: "Implement and document entry controls and visitor logs."
  - id: PS-2
    text: "Device/media disposal policy implemented"
    weight: 3
    remediation: "Sanitize or destroy media per NIST; keep certificates of destruction."

technical:
  - id: TS-7
    text: "Access control (MFA for admins; least privilege)"
    weight: 5
    remediation: "Enable MFA for admins and enforce least-privilege access reviews."
  - id: TS-8
    text: "Transmission security (TLS enforced end to end)"
    weight: 4
    remediation: "Use TLS 1.2+ for all data in transit; disable weak ciphers."
  - id: TS-9
    text: "Audit controls (logs retained ≥ 6 years for HIPAA docs; 1+ year for infra)"
    weight: 3
    remediation: "Retain system logs centrally; ensure CloudTrail/Config retention meets policy."
"""

def run_questionnaire(yaml_path: Optional[str]) -> List[Finding]:
    data = yaml.safe_load(DEFAULT_QUESTIONNAIRE) if not yaml_path else yaml.safe_load(open(yaml_path, "r", encoding="utf-8"))
    findings: List[Finding] = []

    # Interactive or auto? We’ll prompt in terminal for Y/N.
    def ask(item):
        while True:
            ans = input(f"{item['text']} [y/n]: ").strip().lower()
            if ans in ("y","n"): return ans == "y"

    sections = []
    for section_name in ("administrative","physical","technical"):
        if section_name not in data: continue
        print(f"\n-- {section_name.upper()} --")
        for item in data[section_name]:
            ok = ask(item)
            findings.append(Finding(
                item["id"], item["text"],
                "HIGH" if item.get("weight",1) >= 4 else "MEDIUM" if item.get("weight",1) >= 3 else "LOW",
                ok,
                "Implemented" if ok else "Not implemented",
                item.get("remediation","Add remediation details.")
            ))

    return findings

# ------------------------- CLI -------------------------
def main():
    parser = argparse.ArgumentParser(description="HIPAA helper: quick AWS checks + questionnaire (not legal advice).")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("aws", help="Run AWS checks (technical safeguards)")
    p1.add_argument("--profile", default=None, help="AWS profile name (e.g., cloudticity-demo)")
    p1.add_argument("--region", default=None, help="AWS region (e.g., us-west-2)")
    p1.add_argument("--json", action="store_true", help="Output JSON instead of table")

    p2 = sub.add_parser("questionnaire", help="Run an interactive safeguards checklist")
    p2.add_argument("--file", help="YAML file with checklist; default built-in")

    args = parser.parse_args()

    try:
        if args.cmd == "aws":
            findings = run_aws_checks(args.profile, args.region)
            if args.json:
                print(json.dumps([asdict(f) for f in findings], indent=2))
            else:
                acct_info = f"AWS checks (profile={args.profile or 'default'}, region={args.region or 'default'})"
                print_report(findings, acct_info)
        elif args.cmd == "questionnaire":
            findings = run_questionnaire(args.file)
            print_report(findings, "HIPAA Safeguards Questionnaire")
    except Exception as e:
        print(Fore.RED + "Error: " + str(e) + Style.RESET_ALL)
        if sys.gettrace():  # show traceback if in debugger
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
