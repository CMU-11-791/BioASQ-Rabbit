import logging
from logging import config

from Expander import NoneExpander
from SnomedctExpander import SnomedctExpander
from UMLSExpander import UMLSExpander

logging.config.fileConfig('logging.ini')

if __name__ == "__main__":
    # Launch the tasks
    logger = logging.getLogger('main')
    tasks = []
    for cls in (NoneExpander, SnomedctExpander, UMLSExpander):
        instance = cls()
        tasks.append(instance)
        logger.info('Staring service %s', cls.__name__)
        instance.start()

    # And wait for them to terminate
    logger.info('Waiting for the tasks to end.')
    for task in tasks:
        task.wait_for()

    logger.info('Done.')

