# IAM Password Auditor
A python boto3 tool that audits IAM users in an AWS account and reports on password age and flags with severity levels.

## Project Structure 
```
iam-password-auditor/
├── iam-password-auditor.py
└── README.md
```
## Usage
Requires AWS credentials configured on local machine (`~/.aws/credentials`).

```bash
python3 iam-password-auditor.py
```

## Example Output
```text
Password Auditor
=========================
username-demo:
  - Password is 92 days old. Please Change.
```