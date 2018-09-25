import sys
import time
import socket
import threading
import subprocess
from contextlib import closing


def exit(message, code=1):
    print(message, file=sys.stderr)
    sys.exit(code)


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


def spawn_bg_process(*args, queue=None, **kwargs):
    if queue is not None:
        kwargs['stdout'] = subprocess.PIPE
        kwargs['stderr'] = subprocess.PIPE

    p = subprocess.Popen(*args, **kwargs)

    if queue is not None:
        LineReaderThread(p.stdout, queue, (p, 'stdout')).start()
        LineReaderThread(p.stderr, queue, (p, 'stderr')).start()

    return p


class LineReaderThread(threading.Thread):
    def __init__(self, fp, queue, item_prefix):
        super().__init__(daemon=False)
        self.fp = fp
        self.queue = queue
        self.item_prefix = item_prefix

    def run(self):
        for line in self.fp:
            self.queue.put(self.item_prefix + (line,))
        self.queue.put(self.item_prefix + (None,))
