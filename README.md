# CMU 11-791
## BioASQ

This project contains a number of modules to be used as a starting point for the [BioASQ](http://bioasq.org) challenge:

**deiis**<br/>
Utility classes for reading/writing the BioASQ JSON format and working with RabbitMQ message queues.

**Splitter**<br/>
Not currently used.  A future version of this project will perform sentence splitting and tokenization as a distinct step in the pipeline to eliminate the redundant processing.

**Expander**<br/>
Expands medical terms and codes using either [Snomed](https://www.snomed.org) or [UMLS](https://semanticnetwork.nlm.nih.gov).

**Ranker**<br/>
Ranks candidate answers.

**Tiler**<br/>
Combines candidate answers into a final answer.

**Results**<br/>
Collates the results from the pipeline and writes to an output file.

# Contents

1. [Installation](#installation)
1. [Running](#running)
1. [Design Notes](#design-notes)
1. [TODO](#todo)

## Prequisites and Installation

The system configuration for this project is exactly the same as for the [BioasqArchitecture](https://github.com/CMU-11-791/BioasqArchitecture) project. If you have that project working this project will (should) work as well.

1. Python 2.7+
1. Java 1.8
1. Docker (for the RabbitMQ server at least)
1. Pylucene 6.5.0
1. pymetamap (note public_mm must be install separately)
1. SnomedCT data (download link/instructions needed)
1. Other (??)

### Python Dependencies

The `deiis` package must be installed by running the `setup.py` script.

```bash
cd deiis
python setup.py install
cd -
```

Install all of the following with `pip`

1. pymedtermino
1. nltk
1. sklearn
1. werkzeug
1. lxml
1. diskcache
1. pyquery
1. pika

Since the services are no longer web services the following packages are likely no longer required. Although installing them likely does not hurt.

1. flask
1. jinja2
1. itsdangerous
1. click
1. cssselect

# Running

## Start RabbitMQ

If you do not have the RabbitMQ server already running on your machine you will need to start it.  Fortunately, the RabbitMQ server is distributed as a Docker image so no installation or setup is required.

```bash
docker run -d -p 5672:5672 -p 15672:15672 --hostname deiss --name rabbit rabbitmq:3-management
```

After the RabbitMQ server has started you can connect to the management console at [http://localhost:15672](http://localhost:15672) (username: *guest*, password: *guest*).

## Starting The Services

Each module has a `service.py` script that is used to start all of the services in that modules. You can either run each module's `service.py` script in its own shell/terminal. Or you can use the `start.sh` script to start all of the services at once.

## Running The Pipeline

Use the `pipeline.py` script to load a BioASQ JSON and send each question in the file through the processing pipeline.

```bash
python pipeline.py data/training.json
```

## Saving The Results

The `ResultCollector` service will collect all of the candidate answers, however the service has no way of knowing when all of the questions have been collected.  Therefore the `ResultCollector` service listens for a special message to arrive on its message queue (SAVE) and saves the results when it receives that message.  Use the `save.py` script to send the `SAVE` message to the `ResultCollector` service.  If you do not pass a filename/path to the `save.py` script the results will be written to `/tmp/submission.json`.

```bash
python save.py /home/user/data/submission.json
```

## Shutting Down The Services

All of the services will continue waiting on their message queues until they receive a `DIE` message (the poison pill).  Use the `stop.py` script to kill one or more services.

```bash
python stop.py
```

Individual services can be shut down by specifying a list of services. This is useful during development and testing to restart just the services in a particular module.

```bash
python stop.py expand.none expand.snomed expand.umls
```

**Note** All of the services in a module must be shutdown before that module will exit.  The services in each module are:

1. Expander
    1. **expand.none**
    1. **expand.snomed**
    1. **expand.umls**
1. Ranker
    1. **mmr.core**
    1. **mmr.soft**
    1. **mmr.hard**
1. Tiler
    1. **tiler.concat**
1. Results
    1. **results**

**Note** the above names are really the names of the message queues that the service listens to and not the name of the service itself.


# Design Notes

## Messages

Services in the pipeline exchange JSON messages to communicate with each other.  The schema for a message is:

```
class Message
    string type
    object body
    list route
```

Where:

**type**<br/>
Two types of messages are supported: `route` and `command`.  The `command` message type is used to issue a command to a service (shutdown, save, etc.).  The `route` message type contains a question that should be processed and then *routed* to the next service in the pipeline.

**body**<br/>
The body of the message; either the question to be processed (`route` message) or the command to perform (`command` messages).

**route**<br/>
A list of services (message queues) the message should be sent to.  After processing a message it is up to the service to send it to the next service in the list.  If the `route` list is empty the message is dropped (presumably processing the message had some side effects).

Use the `deiis.rabbit.Message` class to create and send messages:

```python
from deiis.rabbit import Message, MessageBus
from deiis.model import Question

question = Question(...)
message = Message(body=question, route=['mmr.soft', 'tiler.concat', 'results'])
bus = MessageBus()
bus.publish('expand.umls', message)
```

## Tasks

All of the services extend the `deiis.rabbit.Task` class which manages the RabbitMQ message queues and starts the message queue listener in its own thread.  The `Task` class will call the `perform` whenever a message arrives on its message queue. Subclasses can override this method to process messages (questions) when they arrive.

The `Task` constructor takes the name of the message queue that that the service will monitor.

```
from deiis.rabbit import Task, Message, MessageBus
from deiis.model import Serializer
from nltk import sent_tokenize, word_tokenize

class Splitter(Task):
    def __init__(self):
        super(Splitter, self).__init__('splitter')

    def perform(self, input):
        """The input is expected to be a JSON string that can be parsed into a Message object"""
        message = Serializer.parse(input, Message)
        message.body = sent_tokenize(message.body)
        self.deliver(message)


class Tokenizer(Task):
    def __init__(self):
        super(Tokenizer, self).__init__('tokenizer')

    def perform(self, input):
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
        message = Serializer.parse(input, Message)
        for sentence in message.body:
            for token in sentence:
                print token
            print ''

```

To invoke the above services:

```python
from deiis.rabbit import Message, MessageBus

message = Message(body="Goodbye cruel world. I am leaving you today.", route=['tokenizer', 'printer'])
bus = MessageBus()
bus.publish('splitter', message)
```

**Note** The code for the above example can be found in `examples/splitter.py`.


# TODO

1. Credentials used to access the UMLS server are hard coded!  These should be loaded from environment variables set on the server. They **should not** be loaded from an *.ini* file that will be checked into source control.
1. Implement the `Splitter` services. Currently the `Ranker` module (in particular the code the calculates similarity scores) performs sentence splitting and tokenizing every time two sentences are compared.  This results in approximately *O(N<sup>2</sup>)* tokenizations being performed when *O(N)* will do.
1. All of the services assume that the RabbitMQ server is available on *localhost*.  In practice this is likely not to be the case.  The address of the RabbitMQ server should be parameterized and obtained from an *.ini* file or loaded from an environmental variable. E.g:
```python
  host = os.environ.get('RABBITMQ_HOST')
  bus = MessageBus(host=host)
```
4. Deploy all of the services in Docker containers to simplify scaling services on Kubernetes clusters.
1. Better setup instructions/scripts for setting up all the dependencies.



