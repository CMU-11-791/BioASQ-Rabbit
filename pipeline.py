#!/usr/bin/env python

import sys
from deiis.rabbit import Message, MessageBus
from deiis.model import Serializer, DataSet, Question

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Usage: python pipeline.py <data.json>'
        exit(1)

    # filename = 'data/training.json'
    filename = sys.argv[1]
    print 'Processing ' + filename
    fp = open(filename, 'r')
    dataset = Serializer.parse(fp, DataSet)
    fp.close()

    # The list of services to send the questions to.
    pipeline = ['mmr.core', 'tiler.concat', 'results']
    count=0
    bus = MessageBus()
    for index in range(0,10):
        question = dataset.questions[index]
    # for question in dataset.questions:
        message = Message(body=question, route=pipeline)
        bus.publish('expand.none', message)
        count = count + 1

    print 'Sent {} questions for ranking.'.format(count)
    print 'Done.'
