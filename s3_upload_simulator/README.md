# s3 upload simulator 
Simulates uploading a file to an s3 bucket. Takes user specified 'test' file and bucket name via CLI arguments and outputs a JSON file with file details. The user is prompted to confirm the upload and this is shown in the JSON file 'status' key as 'success'.

## Project Structure 
```
s3_upload_simulator/
├── s3_simulator.py
├── data/
│   └── test_file.txt
├── logs/
│   └── .gitkeep
├── output/      
│   └── output.json
│   └── .gitkeep
└── README.md
```

## JSON output structure
General file information is stored in the output folder as a .json file. Example entry below:
```json
{
    "uploads": [
        {
            "filename": "allow_list_fixed.txt",
            "bucket": "my-bucket",
            "size_bytes": 158,
            "timestamp": "2026-04-17 13:48:50",
            "status": "success"
        }
    ]
}
```

## How to run
Script uses `pathlib` throughout so paths are resolved to the script location and can be used on any computer. Use the `test_file.txt` in the `data` folder to get started quickly. User confirmation is required `(y/n)` to confirm the simulated upload. An entry will be logged in the output `.json` file. This is read and written each time the script is run so all entries are visible in the same file.

## Example run
Below is an example of user cli arguments with use of test file:

```bash
python3 s3_simulator.py --file data/test_file.txt --bucket my-bucket
```
the user will then be prompted to continue:

```text
Would you like to continue uploading this file to s3 bucket (y/n): 
```
if the user wishes to continue and `y` is selected, the script will complete and the `.json` file will be updated with the latest information.

## Example Output
Terminal output of completion below:

```text
-------------------------------------------------------
TEST_FILE.TXT is being moved to MY-BUCKET: Authorised by user
-------------------------------------------------------

Output file updated with latest file information
```

## Logging
Internal timestamped logging will log INFO, WARNING and ERROR messages to the .log file, example entry below:

```text
2026-04-17 14:21:45 - INFO - TEST_FILE.TXT is being moved to MY-BUCKET: Authorised by user
2026-04-17 14:21:45 - INFO - Output file updated with latest file information
```

## Error handling
- Falls back to console logging if the log file cannot be created.
- exits cleanly with a warning if the specified file does not exist.
- Handles JSONDecodeError if the output file is malformed.
- Validates project folder structure on startup.