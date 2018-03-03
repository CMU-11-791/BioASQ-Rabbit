from deiis.model import DataSet, Question, Serializer
from deiis.rabbit import Task, Message

import logging
from logging import config
logging.config.fileConfig('logging.ini')

try:
    basestring
except:
    basestring = str


class ResultsCollector(Task):
    """
    The last service in any pipeline.  The ResultsCollector collects all the
    ranked sentences in a list object and then writes the list to a file when
    it receives a ``SAVE`` command message.
    """

    def __init__(self, host):
        super(ResultsCollector, self).__init__('results', host)
        self.logger.info('Created Results task')
        self.count = 0
        self.questions = list()

    def perform(self, input):
        question = Question(input)
        self.logger.debug("Received results for question %s", question.id)
        self.questions.append(question)

    def command(self, input):
        if unicode.startswith(input, 'SAVE'):
            self.logger.debug("Received the SAVE command.")
            parts = input.split(' ')
            if len(parts) > 1:
                self.save(parts[1])
            else:
                self.save()
        elif input == 'RESET':
            self.logger.info("Clearing the question list.")
            self.questions = list()
        else:
            self.logger.warn("Unknown command message: %s", input)

    def save(self, path=None):
        if path is None:
            path = '/tmp/submission.json'

        self.logger.debug("Saving dataset to %s", path)
        self.logger.debug("Dataset contains %d questions.", len(self.questions))
        dataset = DataSet()
        dataset.questions = self.questions
        json = Serializer.to_pretty_json(dataset)
        fp = open(path, 'w')
        fp.write(json)
        fp.close()
        self.logger.info("Wrote %s", path)
        self.questions = []