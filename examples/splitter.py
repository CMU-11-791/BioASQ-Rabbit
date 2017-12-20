from deiis.rabbit import Task, Message, MessageBus
from deiis.model import Serializer
from nltk import sent_tokenize, word_tokenize
import time

class Splitter(Task):
    def __init__(self):
        super(Splitter, self).__init__('splitter')

    def perform(self, input):
        """The input is expected to be a JSON string that can be parsed into a Message object"""
        print 'Splitting ' + input
        message = Serializer.parse(input, Message)
        message.body = sent_tokenize(message.body)
        self.deliver(message)


class Tokenizer(Task):
    def __init__(self):
        super(Tokenizer, self).__init__('tokenizer')

    def perform(self, input):
        print 'Tokenizing ' + input
        message = Serializer.parse(input, Message)
        tokenized_sentences = list()
        for sentence in message.body:
            tokenized = word_tokenize(sentence)
            tokenized_sentences.append(tokenized)
        message.body = tokenized_sentences
        self.deliver(message)


class Printer(Task):
    def __init__(self):
        super(Printer, self).__init__('printer')

    def perform(self, input):
        print 'Printing ' + input
        message = Serializer.parse(input, Message)
        for sentence in message.body:
            for token in sentence:
                print token
            print ''

if __name__ == '__main__':
    splitter = Splitter()
    tokenizer = Tokenizer()
    printer = Printer();

    services = (splitter, tokenizer, printer)

    for service in services:
        print 'Staring service ' + str(type(service))
        service.start()

    print 'Sending the message to the splitter'
    message = Message(body="Goodbye cruel world. I am leaving you today.", route=['tokenizer', 'printer'])
    bus = MessageBus()
    bus.publish('splitter', message);

    print 'Sleeping...'
    time.sleep(1)

    print 'Stopping all the services'
    for service in services:
        service.stop()

    print 'Done.'

