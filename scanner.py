import socket
import concurrent.futures


def scan_port(target_ip, port):

    try:
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(1)

        result = sock.connect_ex(
            (target_ip, port)
        )

        sock.close()

        if result == 0:
            return True

        return False

    except Exception:
        return False


def scan_single_port(args):

    target_ip, port = args

    if scan_port(target_ip, port):
        return port

    return None


def scan_range(target_ip, start_port, end_port):

    open_ports = []

    ports = [
        (target_ip, port)
        for port in range(start_port, end_port + 1)
    ]

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=100
    ) as executor:

        results = executor.map(
            scan_single_port,
            ports
        )

    for result in results:

        if result is not None:
            open_ports.append(result)

    return sorted(open_ports)