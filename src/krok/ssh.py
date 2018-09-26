import re
import sys
import subprocess

from . import utils

allocated_port_re = re.compile(rb'^Allocated port (\d+) ')


def assert_local_version_supported():
    try:
        result = subprocess.run(['ssh', '-V'], check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        return utils.exit(e)
    if not result.stderr.startswith(b'OpenSSH'):
        return utils.exit("'ssh' is not the OpenSSH client, apparently.")


def spawn_forwarder(local_host, local_port, ssh_host, ssh_port, callback):
    p = subprocess.Popen([
        'ssh',
        '-F', '/dev/null',                       # ignore local configuration (~/.ssh/config)
        '-o', 'StrictHostKeyChecking=no',        # don't validate host key:
        '-o', 'UserKnownHostsFile=/dev/null',    # don't store host key:
        '-N',                                    # no remote command, just forward ports
        '-T',                                    # don't allocate a tty
        '-o', 'ServerAliveInterval=1',           # ping once a second
        '-o', 'ServerAliveCountMax=10',          # disconnect after ten ping failures
        '-R', f'*:0:{local_host}:{local_port}',  # listen on free port and forward connections to local
        '-p', str(ssh_port),                     # ssh server port (forwarded to localhost)
        f'krok@{ssh_host}'                       # login as "krok"
    ], stderr=subprocess.PIPE)

    callback_called = False
    for ssh_line in p.stderr:
        if ssh_line.startswith(b'Warning: Permanently added'):
            continue

        if not callback_called:
            m = allocated_port_re.match(ssh_line)
            if m:
                remote_port = int(m.group(1))
                callback(remote_port)

        sys.stderr.buffer.write(ssh_line)
