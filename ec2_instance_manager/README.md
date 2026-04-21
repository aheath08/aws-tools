# EC2 Instance Manager
Simulates stopping  EC2 instances that have been flagged with `KeepRunning=False` in their config files. Uses test config files to show successful move. Dry run CLI argument also an option. In a real run, instances that have been identified as needing to be stopped will be permanently moved to the `stopped_instances` folder.

## Project Structure 
```
ec2_instance_manager/
├── stop_instances.py
├── logs/
│   └── .gitkeep
├── running_instances/
│   ├── instance_1/
│   │   └── config.txt
│   ├── instance_2/
│   │   └── config.txt
│   └── instance_3/
│       └── config.txt
├── stopped_instances/
│   └── .gitkeep
└── README.md
```

## How to Run
Script uses `pathlib` throughout so paths are resolved to the script location and can be used on any computer. Optional `--dry-run` cli argument can be passed to check the script without moving the `config.txt` files. Each config.txt file contains text stating whether or not it needs to be stopped, example below:
```text
Name=web-server
KeepRunning=false
```
To run a dry run, run the script as follows:
```bash
python3 stop_instances.py --dry-run
```
To see the files move successfully, run the script as follows:
```bash
python3 stop_instances.py
```
The user will then be prompted to confirm the move:
```text
⚠️ This will move instances. Are you sure? (y/n): 
```
User will then receive confirmation either way.

## Example Output
Aborted example output and successful output shown below:
```text
⚠️ This will move instances. Are you sure? (y/n): n

ABORTED: Script has been aborted by user
```
```text
⚠️ This will move instances. Are you sure? (y/n): y

⚠️ INSTANCE_3 FOUND | Action: to be stopped

✅ INSTANCE_3 moved successfully

⚠️ INSTANCE_1 FOUND | Action: to be stopped

✅ INSTANCE_1 moved successfully
```

## Logging
Internal timestamped logging will log INFO, WARNING and ERROR messages to the .log file, example entry below:

```text
2026-04-21 18:26:53 - INFO - INSTANCE_1 FOUND | Action: to be stopped
2026-04-21 18:26:53 - INFO - INSTANCE_1 moved successfully
```

## Error Handling
- Falls back to console logging if the log file cannot be created.
- Exits cleanly with a warning if running_instances doesn't exist.
- If one of the config files cannot be read, raises error but continues. 
- Raises and logs a subprocess error if the move operation fails.