import argparse

from . import ssh
from . import utils
from .kubectl import KubeCtl


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-n', '--namespace',
                            help='Kubernetes namespace for the service')

    arg_parser.add_argument('-l', '--local-host', default='127.0.0.1',
                            help='Host to forward incoming connections (defaults to 127.0.0.1)')
    arg_parser.add_argument('-p', '--local-port',
                            help='Port to forward incoming connections (defaults to service port)')

    arg_parser.add_argument('service_name',
                            help='Kubernetes service name')
    arg_parser.add_argument('service_port',
                            help='Kubernetes service port')

    args = arg_parser.parse_args()

    ssh.assert_local_version_supported()
    KubeCtl.assert_version_supported()

    kubectl = KubeCtl(namespace=args.namespace)
    pod = get_server_pod_name(kubectl)
    print(pod)


def get_server_pod_name(kubectl):
    pods = kubectl('get', 'pods', '-l', 'run=krok', '-o', 'jsonpath={.items[*].metadata.name}').splitlines()
    if len(pods) < 1:
        return utils.exit(f'krok server is not installed in namespace "{kubectl.namespace}"')
    if len(pods) > 1:
        return utils.exit(f'krok server has more then one pod in namespace "{kubectl.namespace}"')
    return pods[0]


if __name__ == '__main__':
    main()
