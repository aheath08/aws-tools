# IAM Policy Analyser

A Python CLI tool that reads AWS IAM policy JSON documents and analyses them for potential security risks and provides policy breakdown.

## Version 
Current: v1.0 - basic policy analysis and wildcard detection 

## Project Structure
```
iam-policy-analyser/
├── iam-policy-analyser.py
├── data/
│   └── policies.json
├── logs/
│   └── .gitkeep
└── README.md
```

## Features
- Counts total policies 
- Breaks down Allow and Deny statements
- Flags policies with wildcard actions ('*') as potentially dangerous
- Structured logging with log file and console fallback

## JSON Structure 
```json
   [ {
        "PolicyName": "S3ReadOnly",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject", "s3:ListBucket"],
                "Resource": "*"
            }
        ]
    },
    {
        "PolicyName": "EC2FullAccess",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["ec2:*"],
                "Resource": "*"
            }
        ]
    } ]

```

## Example Usage 
A policies.json document is provided to use as a demo as shown in the example run below. But otherwise `--policy-path /path/to/policies.json`.

```bash
python3 iam-policy-analyser.py --policy-path data/policies.json
```

## Example Output
```text
IAM Policy Analyser
------------------------------
Total policies: 3

Allow statements: 2
Deny statements: 1

⚠️ Potentially dangerous policies (wildcard actions): 
 - EC2FullAccess
 - DenyAll

✅ Restricted Policies: 
 - S3ReadOnly
 ```

## Requirements
- python3
- Standard libraries only

## Logging 
Logs are written to 'logs/policy-analyser.log'
Falls back to console output if log directory cannot be created.

```text
2026-06-03 00:27:44 - INFO - Total count logged: 3
2026-06-03 00:27:44 - INFO - Allow statements found: 2
2026-06-03 00:27:44 - INFO - Deny statements found: 1
2026-06-03 00:27:44 - WARNING - wildcard actions found! - DenyAll
```

## Context
Built while studying AWS Solutions Architect Associate — 
demonstrates understanding of IAM policy structure and 
security best practices.

## Future Development
- [ ] Severity levels (Critical/High/Medium/Low) based on policy combination
- [ ] Resource wildcard detection (`"Resource": "*"`)
- [ ] Sensitive service flagging (IAM, S3, KMS, STS)
- [ ] NotAction detection
- [ ] Condition check — flag policies missing conditions
- [ ] Overall risk score
- [ ] JSON report output option (`--output` flag)