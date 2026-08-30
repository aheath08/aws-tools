from botocore.exceptions import NoCredentialsError, ClientError
import boto3

PORTS = [22, 3306, 5432]

def security_audit():
    """Fetch all security groups and return their rules, flagged by port and CIDR."""

    try:
        client = boto3.client('ec2')
        response = client.describe_security_groups()
    except NoCredentialsError as e:
        print(f"Credentials Error: {e}")
    except ClientError as e:
        print(f"Client Error: {e}")

    sg_dict = {}

    for entry in response['SecurityGroups']:
        name = entry['GroupName']
        rules = []

        for rule in entry['IpPermissions']:
            port = rule.get('FromPort', 'All')
            for ip_range in rule.get('IpRanges', []):
                cidr = ip_range.get('CidrIp', '')
                rules.append({'port': port, 'cidr': cidr})

        sg_dict[name] = {'description': entry['Description'], 'rules': rules}
        
    return sg_dict

def main():

    sg_dict = security_audit()

    print(f"\nSecurity Group Report")
    print("=" * 30)

    for _, info in sg_dict.items():
        print(f"\nDescription: {info['description']}")
        high_risk = False
        for e in info['rules']:
            if e['port'] in PORTS and e['cidr'] == "0.0.0.0/0":
                print(f"   - ⚠️ Security Risk: Port {e['port']} OPEN to {e['cidr']}")
                high_risk = True
        if not high_risk:
            print(f"   - No Security Risks Found")

if __name__ == '__main__':
    main()