# import logging
# from logging.config import fileConfig
# logging.config.fileConfig('logging.ini')

import os, sys

from CoreMMR import CoreMMR
from SoftMMR import SoftMMR
from HarderMMR import HarderMMR

if __name__ == '__main__':
    host = os.environ.get('RABBIT_HOST', 'localhost')
    if len(sys.argv) > 1 and sys.argv[1] != '/bin/bash':
        host = sys.argv[1]

    print 'Declaring the services'
    services = list()
    services.append(CoreMMR(host))
    services.append(SoftMMR(host))
    services.append(HarderMMR(host))

    print 'Staring the services'
    for service in services:
        service.start()

    print 'Waiting for the services to terminate'
    for service in services:
        print 'Waiting for service {}'.format(service.__class__.__name__)
        service.wait_for()

    print 'Done.'
