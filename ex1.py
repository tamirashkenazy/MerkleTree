import sys
from hashlib import sha256


class ArgumentsHandler(object):
    def __init__(self, args):
        self.args = args

if __name__ == "__main__":
    args = sys.argv[1:]