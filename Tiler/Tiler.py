# import abc
# from abc import abstractmethod
import abc
from abc import abstractmethod

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
    __metaclass__ = abc.ABCMeta
    def __init__(self, route, host):
        super(Tiler, self).__init__(route, host)

    # abstract method that should be implemented by the subclass that extends this abstract class
    @abstractmethod
    def tileSentences(self, sentences):
        pass

    def perform(self, map):
        # message = Serializer.parse(input, Message)
        question = Question(map)
        # TODO What about the ideal answer task?
        question.exact_answer = self.tileSentences(question.ranked)
        # question.body = question

        # self.logger.debug('Delivering the message to next target')
        # self.deliver(message)
        return question


'''
instance = Tiler(["John"," has cancer"])
print instance.sentenceTiling()
'''
