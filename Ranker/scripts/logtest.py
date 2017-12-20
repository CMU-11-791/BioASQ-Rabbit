import logging
from logging import config
from deiis.rabbit import Task

logging.config.fileConfig('testlog.ini')

def getLogger(obj):
    if isinstance(obj, basestring):
        return logging.getLogger(obj)
    return logging.getLogger(obj.__class__.__name__)

def root_test():
    logger = getLogger('root')
    logger.debug('root debug')
    logger.info('root info')
    logger.warn('root warn')

def rank_test():
    logger = getLogger('rank')
    logger.debug('rank debug')
    logger.info('rank info')
    logger.warn('rank warn')

def core_test():
    logger = getLogger('core')
    logger.debug('core debug')
    logger.info('core info')
    logger.warn('core warn')

class LoggerTest(Task):
    def __init__(self):
        super(LoggerTest, self).__init__('test')

    def test(self):
        self.logger.debug('class debug')
        self.logger.info('class info')
        self.logger.warn('class debug')


root_test()
rank_test()
core_test()
LoggerTest().test()
