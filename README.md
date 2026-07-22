# AWS Tools
A collection of Python boto3 tools for auditing and monitoring AWS account security. Built whilst studying for the AWS Solutions Architect certification.

### IAM Access Key Auditor
Audits IAM users and reports on access key status and age, flagging keys older than 90 days.

### IAM Password Auditor
Audits IAM user passwords and flags by age severity with tiered warnings.

## Requirements
- Python 3
- boto3
- AWS credentials configured (`~/.aws/credentials`)