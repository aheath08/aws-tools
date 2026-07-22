# IAM Access Key Auditor
A python boto3 tool that audits IAM users in an AWS account and reports on access key status and age.

## Project Structure 
```
iam-access-key-auditor/
├── iam-access-key-auditor.py
└── README.md
```

## Usage 
Requires AWS credentials configured on local machine (`~/.aws/credentials`).

```bash
python3 iam-access-key-auditor.py
```

## Example Output
``` text
IAM User Report
------------------------------
User: username-demo
------------------------------
    Key:    "Access Key ID"
    Status: Active
    Age:    98
    Flag:   ⚠️ Older than 90 days
```