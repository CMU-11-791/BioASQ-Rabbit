#!/usr/bin/env python

import sys
from deiis.rabbit import Message, MessageBus

destination = '/tmp/submission.json'
if len(sys.argv) > 1:
    destination = sys.argv[1]

message = Message.Command('SAVE ' + destination, [])

bus = MessageBus()
bus.publish('results', message)
print 'Save command sent. Saving to ' + destination
