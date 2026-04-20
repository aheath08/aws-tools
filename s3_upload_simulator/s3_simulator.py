import logging
from pathlib import Path
from datetime import datetime
import json
import argparse
import sys

# Paths resolve relative to script location so script will work on any machine
LOG_DIR = Path(__file__).parent / "logs"
log_path = LOG_DIR / "s3_simulator.log"
OUTPUT_DIR = Path(__file__).parent / "output"
output_json_path = OUTPUT_DIR / "output.json"

try:
    # If logging setup fails, falls back to console logging so you can still see errors
    log_path.parent.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
except Exception as e:
    logging.basicConfig(level=logging.INFO)
    logging.error(f"Could not set up logging, falling back to console: {e}")

parser = argparse.ArgumentParser(description="Enter file path to be uploaded to s3")
# Type = Path so string is converted to Path object 
parser.add_argument("--file", required=True, type=Path, help="Enter file path")
parser.add_argument("--bucket", required=True, help="Enter s3 bucket name")

def sim_upload(file, bucket_name):

    # Exits early if file does not exist before prompting the user
    if not file.exists():
        logging.error(f"File not found: {file}")
        print(f"⚠️ File not found: {file}")
        sys.exit(1)

    # Case insensitive check so "Y" and "y" both worth as confirmation
    confirm = input(f"Would you like to continue uploading this file to s3 bucket (y/n): ")
    if confirm.lower() != "y":
        logging.warning(f"User cancelled upload: {file} to {bucket_name}")
        print(f"User cancelled upload: {file} to {bucket_name}")
        sys.exit(0)
    
    else:
        print("-" * 55)
        logging.info(f"{file.name.upper()} is being moved to {bucket_name.upper()}: Authorised by user")
        print(f"{file.name.upper()} is being moved to {bucket_name.upper()}: Authorised by user")
        print("-" * 55)
        return True
    
def save_record(file, bucket_name):

    # Build new upload record - timestamp captured at write time not script start
    new_entry = {
        "filename": file.name,
        "bucket": bucket_name,
        "size_bytes": file.stat().st_size,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "success"
    }

    output_json_path.parent.mkdir(exist_ok=True)

    if output_json_path.exists():
        try:
            with open(output_json_path, "r")as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"Error loading JSON file, {e}")
            print(f"Error loading JSON file, {e}")
    
    else:
        data = {"uploads": []}
    
    data["uploads"].append(new_entry)

    with open(output_json_path, "w") as file:
        json.dump(data, file, indent=4)

def main ():

    args = parser.parse_args()

    # Only save record if upload was confirmed and successful
    if sim_upload(args.file, args.bucket):
        save_record(args.file, args.bucket)
        logging.info(f"Output file updated with latest file information")
        print(f"\nOutput file updated with latest file information")

if __name__ == "__main__":
    main()