import socket


def grab_banner(host, port):

    try:
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(2)

        sock.connect((host, port))

        if port == 80:

            sock.send(
                b"HEAD / HTTP/1.0\r\n\r\n"
            )

        banner = sock.recv(1024)

        sock.close()

        return banner.decode(
            errors="ignore"
        ).strip()

    except Exception:

        return "No Banner Available"