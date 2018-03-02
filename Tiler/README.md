# CMU 11-791
## DEIIS

The `deiis` package contains two modules:

1. **model** the data model and supporting classes for serializing the BioASQ JSON format.
1. **rabbit** classes to simplify using RabbitMQ message queues. RabbitMQ is easy enough to use, but it does require enough boilerplate that it makes sense to refactor those parts into separate classes.

### Installation

Installation is done by a Python `setup.py` script:

```bash
python setup.py install
```

This is a typical Python setup script and it will install the package into the current environment.  If you are running the BioASQ program(s) in a virtual environment (recommended) be sure to *activate* the environment before running the `setup.py` script.


## JSON Serialization

**Type**<br/>
The `Type` class contains nothing but static factory methods that are used to create default values for missing properties when creating one of the data model classes.

**JsonObject**<br />
The base class for all classes that are serialized to JSON.  The `JsonObject` class contains a `__json_model__()` that subclasses can override to customize the JSON generated for the class.  The default implementation returns `self.__dict__`, which is sufficient for most classes. The `JsonObject` class also provides a constructor that initializes the instance from a `dict` object if provided.

**Serializer**<br/>
To ensure instances are serialized consistently the `Serializer` class is always used to read/write JSON. The `Serializer` class provides a custom [JSONEncoder](https://docs.python.org/2/library/json.html#json.JSONEncoder) that checks if the instance to be serialized contains a `__json_model__()` method. If the method exists it will be used to generate the model to be serialized. Otherwise the default `JSONEncoder` will be used.


## The Data Model

1. `DataSet`
1. `Question`
1. `Snippet`
1. `Sentence`
1. `Triple`

The `DataSet` class represents the list of questions the comprise the entire JSON file.  The BioASQ JSON format does not actually include a `Sentence` field.  However, a future version of this project will perform sentence splitting and tokenization as a separate step to prevent the *O(N<sup>2</sup>)* performance hit from repeatedly calling `sent_tokenize` and `word_tokenize` methods when ranking candidate answers.

## RabbitMQ

The `deiis.rabbit` module contains utility classes for working with most of the RabbitMQ exchange types.  However, this project only uses the `MessageBus` class for sending messages, and the `BusListener` class for receiving messages.

There is also a `Task` class that manages the `MessageBus` and `BusListener` instances as well as running the listener in its own thread.

