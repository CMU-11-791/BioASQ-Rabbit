from deiis.rabbit import Task, Message
from deiis.model import Serializer, Question, Sentence
#from deiis.json import Serializer, Message

from nltk import word_tokenize, sent_tokenize


class Splitter(Task):
    def __init__(self):
        super(Splitter, self).__init__('splitter')

    def perform(self, input):
        message = Serializer.parse(input, Message)
        if message.type == 'command':
            if message.body == 'DIE':
                self.logger.info("Received command message DIE")
                self.stop()
            else:
                self.logger.error('Unknown command message: %s', message.body)

            self.deliver(message)

        question = Question(message.body)
        question.tokens = word_tokenize(question.body)
        for snippet in question.snippets:
            snippet.sentences = self.tokenize(snippet.text)

        message.body = question
        self.deliver(message)

    def tokenize(self, text):
        sentences = []
        for s in sent_tokenize(text):
            sentence = Sentence(s)
            sentence.tokens = word_tokenize(s)
            sentences.append(sentence)
        return sentences