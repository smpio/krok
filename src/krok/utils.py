import sys


def exit(message, code=1):
    print(message, file=sys.stderr)
    sys.exit(code)
