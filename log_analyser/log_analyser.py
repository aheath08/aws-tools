from datetime import datetime
from collections import Counter
import argparse
from pathlib import Path
import json
import logging
import sys

# Paths resolve relative to script location so script works on any machine
data_file_path = Path(__file__).parent / "data" / "aws_logs.json"
logging.basicConfig(
    filename=Path(__file__).parent / "logs" / "aws_service.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
# Parse CLI arguments, allows flexible filtering of AWS services without modification
def parse_arguments():
    parser = argparse.ArgumentParser(description="Count users by service used")

    parser.add_argument("--service", required=True, help="Enter service e.g. 'EC2'")
    parser.add_argument("--output", help="Optional saves to output file eg. 'service.txt'")

    return parser.parse_args()

def load_logs(file_path):
    # Loads JSON log data from data/aws_logs.json and closes neatly
    # Exits if file missing or malformed to prevent downstream errors
    try:
        with open(file_path, "r")as f:
            logging.info(f"JSON file loaded successfully")
            return json.load(f)
        
    except FileNotFoundError as e:
        print(f"⚠️ Log file not found: {e}")
        logging.warning(f"Log file not found: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"⚠️ Error with JSON file: {e}")
        logging.error(f"Error with JSON file: {e}")
        sys.exit(1)

def filter_service(log_file, service_name):
    # Case insensitive so EC2, ec2 and Ec2 all return the same results 
    return [
        log for log in log_file if log['service'].lower() == service_name.lower()
    ]

def count_users(logs):
    user_counter = Counter([log['user'] for log in logs])
    return user_counter

def format_results(results):
    return " | ".join(f"{user}: {count}" for user, count in results.items())

def save_output(output_file, summary, service):
    # Timestamp captured at write time not start of script
    TIME_NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # File is opened in append mode so you can see previous runs 
    try:
        with open(output_file, "a")as f:
            f.write(f"\n{TIME_NOW}: {service.upper()} | {summary}")
    except IOError as e:
        logging.error(f"Could not write to output file: {e}")
        print(f"Could not write to output file: {e}")


def main():
    # Orchestrates script execution. 
    # - parses arguments
    # - loads data
    # - filters log by service
    # - gets user counts per service 
    # - formats user counts into a compact string for logging and optional file output
    # - outputs to terminal and optional save output file

    args = parse_arguments()
    import_data = load_logs(data_file_path)

    # Validate JSON structure before processing. 
    if "logs" not in import_data or not isinstance(import_data["logs"], list):
        print(f"⚠️ Invalid JSON structure: 'logs' key missing\n")
        logging.error(f"Invalid JSON structure: 'logs' key missing")
        sys.exit(1)

    filtered = filter_service(import_data['logs'], args.service)

    if not filtered:
        print(f"⚠️ No logs found for service: {args.service.upper()}")
        logging.error(f"No logs found for service: {args.service.upper()}")
        sys.exit(1)

    results = count_users(filtered)
    summary = format_results(results)

    logging.info(f"Service searched: {args.service.upper()} | {summary}")
    print(f"\nService: {args.service.upper()}\n")
    print(f"User access counts:")

    for user, count in results.most_common():
        print(f"{user}: {count}")

    # User can create new output folder with new name and the script will not crash as this is handled with Path
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_output(args.output, summary, args.service)
        print(f"\n🗂️ Output file saved to {args.output}")
        logging.info(f"🗂️ Output file saved to {args.output}")


if (__name__) == "__main__":
    main()

  





