# AWS-Tools
A collection of tools created whilst in the early stages of studying the AWS Solutions Architect course. Used to simulate various cloud behaviours. 

## EC2 Instance Manager
Stops instances that are marked as `KeepRunning=False` and moves the files to a `stopped_instances` folder.

## S3 Upload Simulator
Simulates uploading a file to a user defined bucket name. Takes user input to confirm the move and generates JSON file output.

## Log Analyser
Searches JSON file logs and based on cli user inputs will filter the results and optionally save the output.

## Tech Used
- argparse
- logging
- json
- datetime
- pathlib
- subprocess
- collections.Counter
- sys 
- Python

## Notes
Built while studying for AWS Solutions Architect Associate.
boto3 integration planned to replace simulated functionality with real AWS API calls.