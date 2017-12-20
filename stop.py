#!/usr/bin/env python

import sys
from deiis.rabbit import MessageBus, Message

# All the services that may be running.
all = [ 'mmr.hard', 'mmr.soft', 'mmr.core',
        'expand.none', 'expand.snomed', 'expand.umls',
        'tiler.concat',
        'results'
        ]

# The shutdown message for the services.
die = Message.Command('DIE', [])
bus = MessageBus()


if len(sys.argv) > 1:
    if sys.argv[1]  == 'all':
        services = all
    else:
        services = sys.argv[1:]
else:
    services = all

# Send the shutdown message to each of the services.
for service in services:
    print 'Terminating ' + service
    bus.publish(service, die)

print 'Done.'
