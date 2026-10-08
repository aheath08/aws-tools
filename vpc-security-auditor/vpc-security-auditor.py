from botocore.exceptions import ClientError, NoCredentialsError
import boto3
import json

def ip_number(netmask):
    """Figures out available IP addresses from netmask"""

    n_bits = 2** (32 - netmask) -2

    return n_bits

def vpc_info(client):
    """Return VPC id and CIDR for each VPC in account"""

    response = client.describe_vpcs()
    vpc_info = {}

    for vpc in response['Vpcs']:
        id = vpc['VpcId']
        cidr_block = vpc['CidrBlock']
        vpc_info[id] = cidr_block

    return vpc_info

def get_subnets(client, vpc_id):
    
    response = client.describe_subnets(
        Filters = [{'Name': 'vpc-id', 'Values': [vpc_id]}]
    )

    return response['Subnets']

def public_igw(client, subnet_id, vpc_id):
    """Find out if each subnet has a route to an IGW or is a private subnet"""

    response = client.describe_route_tables(
        Filters = [{'Name': 'association.subnet-id', 'Values': [subnet_id]}]
    )

    route_tables = response['RouteTables']

    # If subnet is not assigned to a route table, fall back to default route table.
    if not route_tables:
        response = client.describe_route_tables(
            Filters = [{'Name': 'vpc-id', 'Values': [vpc_id]}, 
                       {'Name': 'association.main', 'Values': ['true']}]
        )

        route_tables = response['RouteTables']

    flag = 'private'
    for rt in route_tables:
        for route in rt['Routes']:
            if route.get('DestinationCidrBlock') == "0.0.0.0/0" and route.get('GatewayId', '').startswith("igw-"):
                flag = "public"

    return flag


def main():
    """Parse arguments and display VPC report"""
    
    try:
        client = boto3.client('ec2')
    except ClientError as e:
        print(f"Account error, {e}")
    except NoCredentialsError as e:
        print(f"Credentials error, {e}")


    vpc = vpc_info(client)
    for vpc_id, vpc_cidr in vpc.items():
        print(f"\nVPC: {vpc_id} ({vpc_cidr})")
        print("-" * 50)

        subnets = get_subnets(client, vpc_id)
        for subnet in subnets:
            subnet_id = subnet['SubnetId']
            az = subnet['AvailabilityZone']
            subnet_cidr = subnet['CidrBlock']
            netmask = int(subnet_cidr.split("/")[1])
            igw = public_igw(client, subnet_id, vpc_id)

            print(f"   {subnet_id:<25}{subnet_cidr:<17}{az:<12}{ip_number(netmask)} IPs available.  {igw.upper()}")


if __name__ == '__main__':
    main()
