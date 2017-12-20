from Tiler import Tiler
from deiis.rabbit import Message
from deiis.model import Serializer
from nltk import word_tokenize

import logging
from logging import config

'''
@Author: Khyathi Raghavi Chandu
@Date: October 17 2017

This code contains the implementation of Abstract method for Tiler.
'''

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('tiler')

'''
This is a subclass that extends the abstract class Tiler.
'''


class Concatenation(Tiler):
    def __init__(self):
        super(Concatenation, self).__init__('tiler.concat')

    # Abstract method from Tiler class that takes a list of sentences as arguments and returns the final summary in a single string.
    def tileSentences(self, sentences):
        logger.info('Tiling sentences ' + str(len(sentences)))
        length = 0
        summaryFinal = ""
        for sentence in sentences:
            # BioAsq ideal generation guideline imposes an upper word limit of 200. The following command maintains that restriction.
            if (len(word_tokenize(sentence)) + length) <= 200:
                summaryFinal += sentence
                length += len(word_tokenize(sentence))
        logger.info('Tiled sentences by concatenating')
        return summaryFinal


if __name__ == '__main__':
    instance = Concatenation()
    print instance.tileSentences(["John"," has cancer"])

