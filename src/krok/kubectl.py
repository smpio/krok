import subprocess

from . import utils


class KubeCtl:
    def __init__(self, namespace=None):
        self._namespace = namespace

    @property
    def namespace(self):
        if self._namespace:
            return self._namespace
        else:
            context = _exec('config', 'current-context', oneline=True)
            ns = _exec('config', 'view', '-o', f'jsonpath={{.contexts[?(@.name == "{context}")].context.namespace}}',
                       oneline=True)
            return ns or 'default'

    def __call__(self, *args, **kwargs):
        if self._namespace:
            args = ('--namespace', self.namespace) + args
        return _exec(*args, **kwargs)

    @staticmethod
    def assert_version_supported():
        try:
            _exec('version')
        except subprocess.CalledProcessError as e:
            return utils.exit(e)


def _exec(*argv, oneline=False):
    stdout = subprocess.run(('kubectl',) + argv, check=True, stdout=subprocess.PIPE).stdout
    if oneline:
        lines = stdout.splitlines()
        if not lines:
            return None
        if len(lines) > 1:
            raise Exception('Expected one line, but got', len(lines))
        return lines[0]
    return stdout
