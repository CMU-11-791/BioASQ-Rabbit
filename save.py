#!/usr/bin/env python

import sys
from deiis.rabbit import Message, MessageBus

destination = '/tmp/submission.json'
if sys.argv:
    destination = sys.argv[0]

message = Message.Command('SAVE ' + destination, [])

bus = MessageBus()
bus.publish('results', message)
print 'Save command sent. Saving to ' + destination
