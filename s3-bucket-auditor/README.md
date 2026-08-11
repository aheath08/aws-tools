# S3 Bucket Auditor
A python boto3 tool that audits S3 buckets in the AWS account and reports on Versioning, Size, Objects, Encryption and Public Access.
An optional argument `--skip-list` skips any unwanted buckets and does not report on them. Full bucket name not necessary, using keywords scans the bucket name for matches and skips.

## Project Structure 
```
s3-bucket-auditor/
├── s3-bucket-auditor.py
└── README.md
```
## Usage
Requires AWS credentials configured on local machine (`~/.aws/credentials`).

```bash
python3 s3-bucket-auditor.py
```
## Example Output
```text
python3 s3-bucket-auditor.py --skip-list cloudtrail

S3 Bucket Security Report
===================================

Bucket: example-name-1
    Versioning     : Not Enabled
    Size           : 2.23 KB
    Objects        : 1
    Encryption     : AES256
    Public Access  : Fully blocked
-----------------------------------

Bucket: example-name-2
    Versioning     : Enabled
    Size           : 0 bytes
    Objects        : 0
    Encryption     : AES256
    Public Access  : Fully blocked
-----------------------------------
```