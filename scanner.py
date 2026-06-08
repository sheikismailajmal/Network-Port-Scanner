import socket


def scan_port(target_ip, port):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.settimeout(1)

        result = sock.connect_ex((target_ip, port))

        sock.close()

        if result == 0:
            return True

        return False

    except Exception:
        return False


def scan_range(target_ip, start_port, end_port):

    open_ports = []

    for port in range(start_port, end_port + 1):

        if scan_port(target_ip, port):
            open_ports.append(port)

    return open_ports