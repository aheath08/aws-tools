from datetime import datetime
import time
import random
from pathlib import Path

DIR_PATH = Path(__file__).parent
FILE_PATH = DIR_PATH/"server.log"

MESSAGES = {
    "INFO": [
        "Health check passed",
        "User login successful",
        "Scheduled backup started",
        "Scheduled backup completed",
        "Server started successfully",
        "Cache cleared successfully",
    ],
    "WARNING": [
        "Disk usage at 82%",
        "Memory usage at 85%",
        "Slow response time detected",
        "Retry attempt for failed request",
    ],
    "ERROR": [
        "Failed to connect to database",
        "Timeout connecting to API",
        "Failed to write to disk",
        "Unhandled exception in request handler",
    ],
}


while True:

    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    key = random.choice(list(MESSAGES.keys()))
    message = random.choice(MESSAGES[key])

    with open(FILE_PATH, "a")as f:
        f.write(f"{date_time}: {key.upper()} - {message}\n")

    time.sleep(random.randint(5,15))