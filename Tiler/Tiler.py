# import abc
# from abc import abstractmethod

from deiis.rabbit import Task, Message
from deiis.model import Serializer, Question

'''
@Author: Khyathi Raghavi Chandu
@Date: October 17 2017

This code contains the abstract class for Tiler.
'''

'''
This is an Abstract class that serves as a template for implementations for tiling sentences.
Currently there is only one technique implemented which is simple concatenation.
'''


class Tiler(Task):
    # __metaclass__ = abc.ABCMeta
    # @classmethod
    def __init__(self, route):
        super(Tiler, self).__init__(route)

    # abstract method that should be implemented by the subclass that extends this abstract class
    # @abstractmethod
    def tileSentences(self, sentences):
        pass

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

        question = Question(message.body)
        question.exact_answer = self.tileSentences(question.ranked)
        message.body = question
        self.logger.debug('Delivering the message to next target')
        self.deliver(message)



'''
instance = Tiler(["John"," has cancer"])
print instance.sentenceTiling()
'''
