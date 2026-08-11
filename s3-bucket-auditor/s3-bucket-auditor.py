import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import sys
import argparse

KB = 1024
MB = 1024 ** 2

def size_format(size):
    """Format a file size in bytes to a readable string."""
    
    if size > MB:
        return f"{size/MB:.2f} MB"
    elif size > KB:
        return f"{size/KB:.2f} KB"
    else:
        return f"{size} bytes"

def bucket_list(skip_list):
    """Scan all S3 buckets and return security configuration details."""

    try:
        s3 = boto3.client('s3')
        response = s3.list_buckets()
    except NoCredentialsError as e:
        print(f"Credential error: {e}")
        sys.exit(1)
    except ClientError as e:
        print(f"AWS error: {e}")
        sys.exit(1)

    bucket_info = {}

    for bucket in response['Buckets']:
        if any(skip in bucket['Name'].lower() for skip in skip_list):
            continue

        objects = s3.list_objects_v2(Bucket=bucket['Name'])     
        versioning = s3.get_bucket_versioning(Bucket=bucket['Name'])

        encryption = s3.get_bucket_encryption(Bucket=bucket['Name'])
        encryption_type = encryption['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']

        public_access = s3.get_public_access_block(Bucket=bucket['Name'])
        config = public_access['PublicAccessBlockConfiguration']
        if all(config.values()):
            public_access_flag = "Fully blocked"
        else:
            public_access_flag = "Not fully blocked"

        status = versioning.get('Status', 'Not Enabled') 

        bucket_name = bucket['Name']
        bucket_size = 0

        if 'Contents' not in objects:
            bucket_info[bucket_name] = {
                'objects': [], 
                'bucket_size': '0 bytes', 
                'versioning': status, 
                'encryption': encryption_type, 
                'public_access_block': public_access_flag
                }
            continue

        for obj in objects['Contents']:
            bucket_size += obj['Size']

        bucket_info[bucket_name] = {
            'objects': [obj['Key'] for obj in objects['Contents']], 
            'bucket_size': size_format(bucket_size), 
            'versioning': status, 
            'encryption': encryption_type,
            'public_access_block': public_access_flag
            }
    
    return bucket_info

def main():
    """Parse arguments and display the S3 security report."""

    parser = argparse.ArgumentParser(description="S3 bucket security checker")
    parser.add_argument("--skip-list", nargs="*", default=[], help="Enter list of bucket(s) to skip")
    args = parser.parse_args()

    bucket_info = bucket_list(args.skip_list)

    print(f"\nS3 Bucket Security Report")
    print("=" * 35)

    for bucket, details in bucket_info.items():
        print(f"\nBucket: {bucket}")
        print(f"    {'Versioning':<15}: {details['versioning']}")
        print(f"    {'Size':<15}: {details['bucket_size']}")
        print(f"    {'Objects':<15}: {len(details['objects'])}")
        print(f"    {'Encryption':<15}: {details['encryption']}")
        print(f"    {'Public Access':<15}: {details['public_access_block']}")
        print("-" *35)


if __name__ == "__main__":
    main()