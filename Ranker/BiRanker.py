'''
@Author: Khyathi Raghavi Chandu
@Date: October 17 2017

This code contains the abstract class for the BiRanker.
'''

import abc
from abc import abstractmethod
from deiis.rabbit import Task, Message
from deiis.model import Question, Serializer

from nltk.tokenize import sent_tokenize, word_tokenize

import logging
from logging import config
logging.config.fileConfig('logging.ini')


class BiRanker(Task):
    """
    This is an Abstract class that serves as a template for implementations for:
    ranking among sentences and ranking with question.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, route=[], alpha=0.5, selected=10):
        super(BiRanker, self).__init__(route)
        self.alpha = alpha
        self.numSelectedSentences = selected
        self.logger.info('Created Task for %s', self.__class__.__name__)

    def perform(self, input):
        self.logger.info("Input received from route %s", self.route)
        message = Serializer.parse(input, Message)
        if message.type == 'command':
            self.logger.debug("Received command message")
            if message.body == 'DIE':
                self.logger.info("Received the poison pill.")
                self.stop()
            else:
                self.logger.warn("Unknown command message: %s", message.body)
        else:
            self.logger.info('Ranking sentences.')
            self.logger.debug("Message body is a %s", str(type(message.body)))
            question = Question(message.body)
            question.ranked = self.getRankedList(question)
            message.body = question

        self.logger.debug('Delivering the message to next target')
        self.deliver(message)

    @abstractmethod
    def getRankedList(self, question):
        pass

    def getSentences(self, question):
        self.logger.debug('Getting sentences for question %s', question.id)
        sentences = []
        # snippetsText = []
        for snippet in question.snippets: #['snippets']:
            text = unicode(snippet.text).encode("ascii", "ignore")
            # snippetsText.append(text)
            if text == "":
                continue
            try:
                sentences += sent_tokenize(text)
            except:
                sentences += text.split(". ")  # Notice the space after the dot
        return sentences

    def computePositions(self, snippets):
        pos_dict = {}
        max_rank = len(snippets)
        rank = 0
        for snippet in snippets:
            snippet = unicode(snippet.text).encode("ascii", "ignore")
            more_sentences = [i.lstrip().rstrip() for i in sent_tokenize(snippet)]
            for sentence in more_sentences:
                if sentence not in pos_dict:
                    pos_dict[sentence] = 1 - (float(rank) / max_rank)
            rank += 1
        self.logger.info('Computed position dictionary for Bi Ranking')
        return pos_dict
