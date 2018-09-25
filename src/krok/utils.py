import sys
import time
import socket
from contextlib import closing


def exit(message, code=1):
    print(message, file=sys.stderr)
    sys.exit(code)


def find_free_port() -> int:
    """
    Find a port that isn't in use.
    XXX race condition-prone.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(('', 0))
        return s.getsockname()[1]
    finally:
        s.close()


def wait_socket(host, port, timeout=None):
    start_time = time.time()

    while True:
        if check_socket(host, port):
            return True
        if timeout is not None and time.time() > start_time + timeout:
            return False


def check_socket(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return sock.connect_ex((host, port)) == 0
