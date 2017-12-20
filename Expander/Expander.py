'''
@Author: Khyathi Raghavi Chandu
@Date: October 17 2017

This is an Abstract Class to perform Concept Expansions. This class cannot be instantiated as all the abstract methods are not
implemented.
The subclass that extends the abstract class is valid if and only if all the abstract methods are implemented.
'''

from deiis.rabbit import Task, Message
from deiis.model import Serializer

from singletonConceptId import *

import logging
from logging import config

logging.config.fileConfig('logging.ini')
# logger = logging.getLogger('bioAsqLogger')


class Expander(Task):
    # __metaclass__ = abc.ABCMeta

    # @classmethod
    def __init__(self, route):  # constructor for the abstract class
        super(Expander, self).__init__(route)
        self.mm = SingletonMetaMap.Instance().mm

    def perform(self, input):
        message = Serializer.parse(input, Message)
        if message.type == 'command':
            self.logger.debug("Received command message")
            if message.body == 'DIE':
                self.logger.info('Received the poison pill')
                self.stop()
                return
            else:
                self.logger.warn("Unknown command message: %s", message.body)
        message.body = self.getExpansions(message.body)
        self.logger.debug('Delivering the message to next target')
        self.deliver(message)


    # This is the abstract method that is implemented by the subclasses.
    # @abstractmethod
    def getExpansions(self, sentence):
        pass

    # Given a sentence as input, this method gives a list of all the biomedical concepts identified by the metamap
    # @classmethod
    def getMetaConcepts(self, sentence):
        self.logger.info('retrieving meta concepts from MetaMap')
        try:
            sents = [sentence]
            cuiList = []
            # Following line is an example of how the variable sents (string) has to be passed into extract_concepts as a list.
            # sents = ['John had a leukemia']# and heart attack']
            # self.mm = SingletonMetaMap.Instance().mm
            metaConcepts, error = self.mm.extract_concepts(sents, [1, 2])
            return metaConcepts
        except Exception as e:
            self.logger.debug('Metamap exception ' + str(e))
            return []


class NoneExpander(Expander):
    def __init__(self):
        super(NoneExpander, self).__init__('expand.none')


    def getExpansions(self, sentence):
        return sentence

    # def perform(self, input):
    #     self.logger.debug('Not expanding input!')
    #     message = Serializer.parse(input, Message)
    #     if message.type == 'command':
    #         if message.body == 'DIE':
    #             self.stop()
    #         else:
    #             self.logger.error("Unknown command message %s", message.body)
    #
    #     self.deliver(message)

# If this part is uncommented in the code and run then it should throw an error because the abstract methods are not implemented.
if __name__ == '__main__':
    instance = NoneExpander("John has cancer")
    print instance.getExpansions()
