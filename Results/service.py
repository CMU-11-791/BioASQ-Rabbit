import os, sys
from ResultsCollector import ResultsCollector

if __name__ == '__main__':
    print 'Starting ResultsCollector'
    host = os.environ.get('RABBIT_HOST', 'localhost')
    if len(sys.argv) > 1 and sys.argv[1] != '/bin/bash':
        host = sys.argv[1]

    task = ResultsCollector(host)
    task.start()
    print 'Waiting for the task to terminate.'
    task.wait_for()
    print 'Done.'
