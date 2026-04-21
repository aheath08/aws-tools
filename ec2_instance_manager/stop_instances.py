from pathlib import Path
import subprocess
import logging
import argparse

# Paths resolve relative to script location so script works on any machine
BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
log_path = LOG_DIR / "instance_manager.log"

parser = argparse.ArgumentParser(description="Enable dry mode option available")
# store_true means flag is either present or not - no value needed
parser.add_argument("--dry-run", action="store_true", help="dry mode will not move any files")
args = parser.parse_args()

try:
    # Fail safe - if logging setup fails, falls back to console so errors are still visible
    log_path.parent.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
except Exception as e:
    logging.basicConfig(level=logging.INFO)
    logging.warning(f"Could not set up log file, falling back to console: {e}")

running_instances = BASE_DIR / "running_instances"
stopped_instances = BASE_DIR / "stopped_instances"

# Fail safe - exits early if running_instances folder does not exist
if not running_instances.exists():
    logging.warning(f"no {running_instances} folder found")
    print(f"No {running_instances} folder found")
    exit(1)

# Only create/check if stopped_instances folder if real run
if not args.dry_run:
    stopped_instances.mkdir(exist_ok=True)

running_processes = []

for instance in running_instances.iterdir():

    # Only process directories - skip any loose files in running_instances
    if not instance.is_dir():
        continue
    
    config = instance / "config.txt"
    if not config.exists():
        logging.error(f"No config file found in {instance}")
        print(f"\nNo config file found in {instance}")
        continue
    
    try:
        content = config.read_text()
    except Exception as e:
        logging.warning(f"Could not read config file: {e}")
        print(f"\nCould not read config file: {e}")
        continue
    
    # Case insensitive so keepRunning=False and KEEPRUNNING=FALSE also match
    if "keeprunning=false" in content.lower():
        running_processes.append(instance)

if args.dry_run:
    print(f"DRY RUN: No files will be moved")
    logging.info(f"DRY RUN: No files will be moved")

if running_processes:

    # Confirm before any destructive action - skipped in dry run mode
    if not args.dry_run:
        confirm = input("\n⚠️ This will move instances. Are you sure? (y/n): ")
        if confirm.lower() != "y":
            print("\nABORTED: Script has been aborted by user")
            logging.info(f"ABORTED: Script aborted by user")
            exit(0)

    for instance in running_processes:
        logging.info(f"{instance.name.upper()} FOUND | Action: to be stopped")
        print(f"\n⚠️ {instance.name.upper()} FOUND | Action: to be stopped")

        if not args.dry_run:
            try:
                # subprocess runs with check=True and raises CalledProcessError if mv fails
                subprocess.run(["mv", str(instance), str(stopped_instances)], check=True)
                logging.info(f"{instance.name.upper()} moved successfully")
                print(f"\n✅ {instance.name.upper()} moved successfully")

            except subprocess.CalledProcessError as e:
                logging.error(f"Could not move {instance.name} | Error: {e}")
                print(f"Could not move {instance.name} | Error: {e}")

else:
    logging.info(f"NO instances found that need stopping")
    print("NO instances found that need stopping")
    