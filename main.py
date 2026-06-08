from logger import log_message
from scanner import scan_range
from service_detector import get_service
from database import create_database, save_scan_result
from datetime import datetime

# Create database and table
create_database()

# Target to scan
target = "scanme.nmap.org"

# Scan ports 20-25
open_ports = scan_range(target, 20, 25)

print("\nOpen Ports Found:\n")

for port in open_ports:
    service = get_service(port)

    print(f"Port {port} OPEN ({service})")
    log_message(f"Port {port} OPEN ({service})")
    save_scan_result(
        target,
        port,
        service,
        "OPEN",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

print(f"\nTotal Open Ports: {len(open_ports)}")