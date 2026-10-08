# VPC Security Auditor
A python boto3 script that audits the public access security of a VPC. If a subnet's associated route table has access to an Internet Gateway it will be flagged as `PUBLIC`. Otherwise it will be flagged as `PRIVATE`. Will also display the available number of IP addresses based on the netmask.

## Project Structure 
```
vpc-security-auditor/
├── vpc-security-auditor.py
└── README.md
```

## Usage
Requires AWS credentials configured on local machine (`~/.aws/credentials`).
```bash
python3 vpc-security-auditor.py
```

## Example Output
```text
VPC: vpc-0243ed252911197c8 (172.31.0.0/16)
--------------------------------------------------
   subnet-id1 172.31.0.0/20    us-east-1a  4094 IPs available.  PUBLIC
   subnet-id2 172.31.80.0/20   us-east-1b  4094 IPs available.  PUBLIC
   subnet-id3 172.31.32.0/20   us-east-1d  4094 IPs available.  PUBLIC
   subnet-id4 172.31.64.0/20   us-east-1f  4094 IPs available.  PUBLIC
   subnet-id5 172.31.48.0/20   us-east-1e  4094 IPs available.  PUBLIC
   subnet-id6 172.31.16.0/20   us-east-1c  4094 IPs available.  PRIVATE
```

- Note that one of the default VPC subnets has been associated with a private route table

## Planned addition:
- Flagging security groups within each VPC that have inbound rules open to 0.0.0.0/0 on sensitive ports.