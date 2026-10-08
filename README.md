# AWS Tools
A collection of Python boto3 tools for auditing and monitoring AWS account security. Built whilst studying for the AWS Solutions Architect certification.

### IAM Access Key Auditor
Audits IAM users and reports on access key status and age, flagging keys older than 90 days.

### IAM Password Auditor
Audits IAM user passwords and flags by age severity with tiered warnings.

### S3 Bucket Auditor
Audits S3 Buckets and prints security report. Includes argparse option to ignore certain buckets based on keywords.

### Security Port Auditor
Audits AWS security groups for certain ports open to CIDR range `0.0.0.0/0`, which could be seen as a security risk.

### VPC Security Auditr
Audits VPC's in an account to see if any associated subnets have access to an internet gateway. Subnet will be flagged as `PUBLIC` if it does or otherwise `PRIVATE`.

## Requirements
- Python 3
- boto3
- AWS credentials configured (`~/.aws/credentials`)