from ResultsCollector import ResultsCollector

if __name__ == '__main__':
    print 'Starting ResultsCollector'
    task = ResultsCollector()
    task.start()
    print 'Waiting for the task to terminate.'
    task.wait_for()
    print 'Done.'
