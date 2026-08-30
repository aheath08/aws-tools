# Security Group Port Auditor
A python boto3 tool that audits the ports in AWS Security Groups. If a rule opens a port listed in the `PORTS` variable to the cidr range `0.0.0.0/0` it will be flagged as a security risk.

## Ports Checked
By default, flags the following ports if open to `0.0.0.0/0`
- 22 (SSH)
- 3306 (MySQL)
- 5432 (PostgreSQL)

## Project Structure 
```
security-port-auditor/
├── security-port-auditor.py
└── README.md
```

## Usage
Requires AWS credentials configured on local machine (`~/.aws/credentials`).
```bash
python3 security-port-auditor.py
```

## Required Permissions
IAM user/role needs `ec2:DescribeSecurityGroups`.

## Example Output
Example run (identifying details redacted):

```text
python3 security-port-auditor.py

Security Group Report
==============================

Description: launch-wizard-2 created 2026-01-01T01:01:01.000Z
   - ⚠️ Security Risk: Port 22 OPEN to 0.0.0.0/0

Description: launch-wizard-1 created 2026-01-01T01:01:01.000Z
   - ⚠️ Security Risk: Port 22 OPEN to 0.0.0.0/0

Description: default VPC security group
   - No Security Risks Found
```