import os, sys
from Concatenation import Concatenation


if __name__ == "__main__":
    host = os.environ.get('RABBIT_HOST', 'localhost')
    if len(sys.argv) > 1 and sys.argv[1] != '/bin/bash':
        host = sys.argv[1]

    print('Starting Tiler services.')
    task = Concatenation(host)
    task.start()
    task.wait_for()


