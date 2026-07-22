import boto3
from datetime import datetime, timezone
from botocore.exceptions import ClientError, NoCredentialsError
import sys


def iam_users():
    """ Audit IAM user access keys and flag any older than 90 days. """

    try:
        iam = boto3.client('iam')
        list_users = iam.list_users()
    except NoCredentialsError as e:
        print(f"Credential error: {e}")
        sys.exit(1)
    except ClientError as e:
        print(f"AWS error: {e}")
        sys.exit(1)

    iam_users_dict = {}

    for user in list_users["Users"]:
        timestamp = datetime.now(timezone.utc)

        username = user['UserName']
        access_keys = iam.list_access_keys(UserName=username)

        key_list = []
        for key in access_keys['AccessKeyMetadata']:

            age = (timestamp - key['CreateDate']).days
            flag = f"⚠️ Older than 90 days" if age > 90 else "✅ less than 90 days"
            status = key['Status']
            key_list.append({
                'key_id': key['AccessKeyId'],
                'age': age,
                'flag': flag,
                'status': status
            })

        iam_users_dict[username] = {
            'keys': key_list
            }   

    return iam_users_dict

def main():

    iam_users_dict = iam_users()

    print(f"\nIAM User Report")
    print("-" * 30)

    for user, data in iam_users_dict.items():

        print(f"User: {user}")
        print("-" *30)

        if not data['keys']:
            print(f"No keys found for this account")
        else:
            for k in data['keys']:
                print(f"    {'Key:':<8}{k['key_id']}")
                print(f"    {'Status:':<8}{k['status']}")
                print(f"    {'Age:':<8}{k['age']}")
                print(f"    {'Flag:':<8}{k['flag']}")

    
if __name__ == '__main__':
    main()