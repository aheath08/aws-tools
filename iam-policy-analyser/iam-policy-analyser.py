import json
import argparse
import sys
import logging
from pathlib import Path

DIR_PATH = Path(__file__).parent
LOG_DIR = DIR_PATH / "logs"
log_path = LOG_DIR / "policy-analyser.log"

try:
    log_path.parent.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
except Exception as e:
    # Logging falls back to console if there is an issue setting up the folder structure.
    logging.basicConfig(level=logging.INFO)
    logging.warning(f"Could not set up file, falling back to console: {e}")


def read_file(path):

    if not path.exists():
        print("No path found!")
        sys.exit(1)
    
    try:
        with open(path, "r") as f:
            data = json.load(f)
        
    except json.JSONDecodeError as e:
        logging.error(f"Json Decode Error: {e}")
        print(f"Error loading JSON file!")
        sys.exit(1)
    
    return data

def count_files(data):
    """
    Analyses IAM policy documents.
    Returns total policy count, allow/deny breakdown and flagged policies. 
    """

    if not data:
        logging.error(f"No data found!")
        print(f"No data found")

    total_count = len(data)
    deny_allow = {"allow": 0, "deny": 0}
    flagged_policies = []

    for entry in data:
        for policy in entry['Statement']:
            # lowercase both sides - Effect could be "Allow" or "allow"
            if policy['Effect'].lower() in deny_allow:
                deny_allow[policy['Effect'].lower()] += 1

            # flag wildcard on Action as this could be overly permissive and a security risk dependent.
            if any("*" in action for action in policy['Action']):
                flagged_policies.append(entry)
    # policies not in flagged list = no wildcard actions found
    restricted = [entry for entry in data if entry not in flagged_policies]

    return total_count, deny_allow, flagged_policies, restricted

def main():

    """
    Entry point - parses CLI arguments and orchestrates analysis.
     type=Path converts string input to Path object automatically. """

    parser = argparse.ArgumentParser(description="Parse and print report from JSON IAM policy")
    parser.add_argument("--policy-path", required=True, type=Path, help="Enter path to JSON file")
    args = parser.parse_args()

    data = read_file(args.policy_path)
    total_count, deny_allow, flagged_policies, restricted = count_files(data)

    print(f"IAM Policy Analyser")
    print("-" * 30)

    if total_count == 0:
        logging.warning(f"No valid total count")
        print(f"No valid total count")
    else:
        print(f"Total policies: {total_count}")
        logging.info(f"Total count logged: {total_count}")

    if not any(deny_allow.values()):
        logging.info(f"No Deny or Allow policies found")
        print(f"No Deny or Allow policies found")
    else:
        print(f"\nAllow statements: {deny_allow['allow']}")
        print(f"Deny statements: {deny_allow['deny']}")
        logging.info(f"Allow statements found: {deny_allow['allow']}")
        logging.info(f"Deny statements found: {deny_allow['deny']}")

    if not flagged_policies:
        logging.info(f"No flagged policies found (no wildcard actions)")
        print(f"No flagged policies found (no wildcard actions)")
    else:
        print(f"\n⚠️ Potentially dangerous policies (wildcard actions): ")
        for flagged in flagged_policies:
            print(f" - {flagged['PolicyName']}")
            logging.warning(f"wildcard actions found! - {flagged['PolicyName']}")
    
    if not restricted:
        logging.info(f"No further issues found")
        print(f"No further issues found")
    else:
        print(f"\n✅ Restricted Policies: ")
        for policy in restricted:
            print(f" - {policy['PolicyName']}")
            logging.info(f"restricted policy found: - {policy['PolicyName']}")

if __name__ == "__main__":
    main()