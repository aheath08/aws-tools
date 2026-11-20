import boto3
from collections import Counter
from botocore.exceptions import NoCredentialsError, ClientError
import argparse
import time
from datetime import datetime
import sys


def log_parsing(client, log_group, log_stream, time_period):

    time_now = time.time()
    start_time_seconds = time_now - (time_period * 60 * 60)

    try:
        response = client.filter_log_events(
            logGroupName=log_group,
            logStreamNames=[log_stream],
            startTime=int(start_time_seconds * 1000),
            endTime=int(time_now * 1000)
        )
    except NoCredentialsError as e:
        print(f"Credentials Error: {e}")
        sys.exit(1)
    except ClientError as e:
        print(f"Client Error: {e}")
        sys.exit(1)

    count = Counter()
    error_list = []
    total_entires = 0

    for event in response['events']:

        parts = event['message'].split()
        severity = parts[2]
        date = parts[0]
        event_time = parts[1].rstrip(":")
        date_time = datetime.strptime(f"{date} {event_time}", "%Y-%m-%d %H:%M:%S")
        message = " ".join(parts[4:])

        if severity.lower() == "error":
            error_list.append({'date_time': date_time,
                               'severity': severity,
                               'message': message
                               })

        total_entires += 1
        count[severity] += 1

    return count, error_list, total_entires


def main(): 

    client = boto3.client('logs')

    parser = argparse.ArgumentParser(description = 'Enter Log Group and Stream to see logs')
    parser.add_argument('--log-group', required=True, type=str, help='Enter name of log group')
    parser.add_argument('--log-stream', required=True, type=str, help='Enter name of log stream')
    parser.add_argument('--time-period', required=True, type=int, help='Enter time period in hours')
    args = parser.parse_args()

    count, error_list, total = log_parsing(client, args.log_group, args.log_stream, args.time_period)

    print(f"\nCloudWatch Log Report - {args.log_group} / {args.log_stream}")
    print(f"Time range: {args.time_period} hour(s)")
    print("=" * 30)
    print(f"Total events: {total}")

    print(f"\nSeverity Breakdown:")
    for level, severity_count in count.items():
        print(f"    {level.upper():<7}: {severity_count}")

    print(f"\n⚠️ Most Recent Errors:")
    sorted_events = sorted(error_list, key=lambda x: x['date_time'], reverse=True)

    for e in sorted_events[0:2]:
        print(f"    {e['date_time']} {e['severity']} {e['message']}")

if __name__ == '__main__':
    main()