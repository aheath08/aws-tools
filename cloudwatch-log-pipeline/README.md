# CloudWatch Log Pipeline
A Python script generates simulated application logs on an EC2 instance, the CloudWatch Agent ships them to
CloudWatch Logs, and a separate boto3 script pulls recent events back out and reports on severity breakdown and the most recent errors.

## Architecture
```
log-generator.py (EC2)
        |
        v
CloudWatch Agent (tails server.log, ships new lines)
        |
        v
CloudWatch Logs (Log Group / Log Stream)
        |
        v
log-report.py (run locally via boto3)
```

## Project Structure
```
cloudwatch-log-pipeline/
├── log-generator.py            # runs on EC2, writes simulated log lines
├── agent-config.json           # CloudWatch Agent config
├── log-report.py               # run locally — pulls and reports on recent log events
└── README.md
```

## 1. Log Generator (`log-generator.py`)
Runs continuously on an EC2 instance, appending a randomly severity-weighted log line (INFO/WARNING/ERROR) to a local file every 5-15 seconds, simulating a live application.

```bash
python3 log-generator.py &
```

## 2. CloudWatch Agent Setup
The EC2 instance's IAM role needs the AWS-managed `CloudWatchAgentServerPolicy` attached.

Install the agent:
```bash
sudo dnf install amazon-cloudwatch-agent -y
```

`agent-config.json` tells the agent which local file to watch and which Log Group / Log Stream to send it to. Start the agent with:

```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/path to agent-config.json -s
```

## 3. Log Report (`log-report.py`)
Run locally (requires AWS credentials configured via `~/.aws/credentials`. No EC2 instance needs to be running, logs persist independently in CloudWatch once shipped).

```bash
python3 log-report.py --log-group cloudwatch-project-logs --log-stream server-log-stream --time-period 24
```

- `--log-group` — required, which CloudWatch Log Group to query
- `--log-stream` — required, which Log Stream within that group to query
- `--time-period` — required, how many hours back to look

## Example Output
```text
CloudWatch Log Report - cloudwatch-project-logs / server-log-stream
Time range: 24 hour(s)
==============================
Total events: 42

Severity Breakdown:
    INFO   : 28
    WARNING: 9
    ERROR  : 5

⚠️ Most Recent Errors:
    2026-10-14 20:48:03 ERROR Failed to connect to database
    2026-10-14 20:41:17 ERROR Timeout connecting to API
```

## Notes
- The report shows only the 2 most recent errors by default — adjust the slice in the script if a longer list is useful.
- `--time-period` is currently required; a sensible future improvement would be making it optional, defaulting to returning all available events when omitted.

## Requirements
- python3
- boto3
- An EC2 instance (for the generator/agent stage only — not required to run `log-report.py` against already-shipped logs)