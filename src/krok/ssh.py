import subprocess

from . import utils


def assert_local_version_supported():
    try:
        result = subprocess.run(['ssh', '-V'], check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        return utils.exit(e)
    if not result.stderr.startswith(b'OpenSSH'):
        return utils.exit("'ssh' is not the OpenSSH client, apparently")
