from botocore.exceptions import NoCredentialsError, ClientError
import boto3
from datetime import datetime, timezone

def get_user_info():
    """Audit IAM user passwords and flag by age severity."""

    try:
        iam = boto3.client('iam')
    except NoCredentialsError as e:
        print(f"Credentials Error: {e}")
    except ClientError as e:
        print(f"Client Error: {e}")
    
    users_list = iam.list_users()

    print(f"\nPassword Auditor")
    print("=" * 25)

    for user in users_list['Users']:
        timestamp = datetime.now(timezone.utc)
        username = user['UserName']

        try:
            details = iam.get_login_profile(
                UserName = username
            )
            create_date = details['LoginProfile']['CreateDate']
            age = (timestamp - create_date).days 
        except iam.exceptions.NoSuchEntityException:
            print(f"{username}: No password set")    
            continue   

        print(f"{username}:")
        if age > 120:
            print(f"  - 🚨 Critical action required. Password is {age} days old.")
        elif age > 90:
            print(f"  - Password is {age} days old. Please Change.")
        elif age > 80:
            print(f"  - Password is approaching {age} days old. Consider changing soon.")
        else: 
            print(f"  - ✅ No password changes required.")
        

if __name__ == '__main__':
    get_user_info()