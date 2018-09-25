import sys
import argparse
import subprocess

from . import ssh
from . import utils
from .kubectl import KubeCtl


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-n', '--namespace',
                            help='Kubernetes namespace for the service')

    arg_parser.add_argument('-l', '--local-host', default='127.0.0.1',
                            help='Host to forward incoming connections (defaults to 127.0.0.1)')
    arg_parser.add_argument('-p', '--local-port', type=int,
                            help='Port to forward incoming connections (defaults to service port)')

    arg_parser.add_argument('service_name',
                            help='Kubernetes service name')
    arg_parser.add_argument('service_port', type=int,
                            help='Kubernetes service port')

    args = arg_parser.parse_args()
    if not args.local_port:
        args.local_port = args.service_port

    ssh.assert_local_version_supported()
    KubeCtl.assert_version_supported()

    kubectl = KubeCtl(namespace=args.namespace)
    pod = get_server_pod_name(kubectl)

    local_ssh_port = utils.find_free_port()
    kubectl.spawn('port-forward', pod, f'{local_ssh_port}:22')

    if not utils.wait_socket('localhost', local_ssh_port, timeout=5):
        utils.exit('krok server not accepting connections')

    try:
        ssh.spawn_forwarder(args.local_host, args.local_port, 'localhost', local_ssh_port, handle_forwarding_started)
    except KeyboardInterrupt:
        return sys.exit(0)


def get_server_pod_name(kubectl):
    pods = kubectl('get', 'pods', '-l', 'run=krok', '-o', 'jsonpath={.items[*].metadata.name}').splitlines()
    if len(pods) < 1:
        return utils.exit(f'krok server is not installed in namespace "{kubectl.namespace}"')
    if len(pods) > 1:
        return utils.exit(f'krok server has more then one pod in namespace "{kubectl.namespace}"')
    return pods[0]


def handle_forwarding_started(remote_port):
    print('YES', remote_port)


if __name__ == '__main__':
    main()
