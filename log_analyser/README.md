# Log analyser
Reads a JSON file and filters the results based on the user service input. Uses logging to capture results as well as optional save output to file.

## Project Structure
```
aws-service-analyser/
├── log_analyser.py
├── data/
│   └── aws_logs.json
├── logs/
│   └── .gitkeep
├── output/          # (optional - generated results, not committed)
└── README.md
```
## JSON data
JSON structure is a list of dictionaries under the key ["logs"]. Example entry:
```py
        {
            "user": "anna",
            "service": "EC2",
            "action": "StartInstances",
            "time": "2026-04-07T14:30:00"
        }
```
## How to run
Script uses `pathlib` throughout so paths are resolved relative to the script 
location — works on any machine without modification. Reads from `data/aws_logs.json` 
and writes logs to `logs/aws_service.log`.

## Example arguments & usage 
Takes service and optional output argument. Specified service must follow --service argument. Output results is optional as seen in example below:

```bash
python3 log_analyser.py --service ec2 --output output/results.txt
```
## Output
Internal timestamped logging will log INFO, WARNING and ERROR messages to the .log file, example entry below:

```text
2026-04-16 12:14:54 - INFO - Service searched: S3 | charlie: 1 | anna: 1
2026-04-16 12:14:54 - INFO - 🗂️ Output file saved to logs/results.txt
```
Optional Output text file will save as shown below. Can create new folder for this as shown in project structure. 

```text
2026-04-16 12:48:28: S3 | charlie: 1 | anna: 1
```
