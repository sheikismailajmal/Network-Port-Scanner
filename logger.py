from datetime import datetime

def log_message(message):
    with open("scan.log", "a") as logfile:
        logfile.write(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n"
        )