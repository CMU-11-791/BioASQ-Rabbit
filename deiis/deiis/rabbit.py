"""
Classes for working with RabbitMQ message queues. Support for three types of
queues is provided.

1. ``MessageQueue`` -- a message queue for implementing the producer/consumer
pattern.
#. ``Broadcaster`` -- used to send messages to all registered listeners.
#. ``MessageBus`` -- used to send messages to a specific listener.

The above classes also have listener classes that users can use to receive
messages.
"""

import pika
import threading
import logging

from deiis.model import Serializer, JsonObject, Type

PERSIST = pika.BasicProperties(delivery_mode=2)

# Python 3 does not have a basestring type. So on Python 3 we assign the 'str'
# type to 'basestring' so we can test if a variable is a string in Python 2 and 3.
try:
    basestring
except:
    basestring = str


class Message(JsonObject):
    """
    The data model for message that are passed between services.

    type -- one of 'route' or 'command'.
    body -- the string (message) to be sent.
    route -- the list of services the message should be sent to.

    Messages of type 'route' should be processed and passed to the next service
    in the ``route`` list.  Messages of type 'command' and used to send commands
    to services, e.g. shutdown.

    """
    properties = {
        'type': (lambda: 'route'),
        'body': Type.text,
        'route': list
    }
    def __init__(self, params=None, **kwargs):
        super(Message, self).__init__(params)
        for name,value in kwargs.iteritems():
            if name in Message.properties:
                setattr(self, name, value)

    def forward(self):
        if len(self.route) == 0:
            return None
        target = self.route[0]
        self.route = self.route[1:]
        return target

    @staticmethod
    def Command(body, route=[]):
        return Message(type='command', body=body, route=route)


class MessageBus(object):
    """
    Creates a 'direct' exchange named 'message_bus'.

    Use a MessageBus instance to send messages to specific listeners on the exchange.

        bus = MessageBus()
        bus.publish('target', 'Hello world.')
    """
    def __init__(self, exchange='message_bus', host='localhost'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange, exchange_type='direct')
        self.exchange = exchange

    def publish(self, route, message):
        if not isinstance(message, basestring):
            message = Serializer.to_json(message)
        try:
            self.channel.basic_publish(exchange=self.exchange, routing_key=route, body=message, properties=PERSIST)
        except Exception as e:
            logger = logging.getLogger(self.__class__.__name__)
            logger.error("Unable to publish the message: %s", e.message)
            logger.exception(e.message)


class BusListener(object):
    """
    A listener for a specific route on the message_bus exchange.

        listener = BusListener('my.address')
        listener.start()

        # In a different thread.
        bus = MessageBus()
        # Send a message to the above listener:
        bus.publish('my.address', 'Hello world.')
    """
    def __init__(self, route, exchange='message_bus', host='localhost'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange, exchange_type='direct')
        self.exchange = exchange
        self.route = route
        result = self.channel.queue_declare(exclusive=True)
        self.name = result.method.queue
        self.channel.queue_bind(exchange=self.exchange, queue=self.name, routing_key=self.route)
        self.logger = logging.getLogger(self.__class__.__name__)

    def start(self):
        """Starts listening on the queue. No messages will be delivered to this
        listener until the `start` method is called.

        This method blocks until another thread calls the `stop` method.
        """
        self.channel.start_consuming()

    def stop(self):
        """Stops the listener and causes the `start()` method to exit."""
        self.logger.debug('Sending basic_cancel')
        self.channel.basic_cancel(self.tag)
        self.logger.debug('basic_cancel sent')

    def register(self, handler):
        self.tag = self.channel.basic_consume(handler, queue=self.name)


class Broadcaster(object):
    """
    Broadcasts messages to all registered listeners.

    Creates a 'fanout' exchange named 'broadcast'.
    """
    def __init__(self, exchange='broadcast', host='localhost'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')
        self.exchange = exchange

    def broadcast(self, message):
        self.channel.basic_publish(self.exchange, routing_key='*', body=message)

    def stop(self):
        self.connection.close()


class BroadcastListener(object):
    """
    A listener for the 'broadcast' exchange.
    """
    def __init__(self, exchange='broadcast', host='localhost'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')
        result = self.channel.queue_declare(exclusive=True)
        self.name = result.method.queue
        self.channel.queue_bind(exchange=exchange, queue=self.name)
        self.tag = False
        self.logger = logging.getLogger(self.__class__.__name__)

    def register(self, handler):
        """
        Register a handler for the exchange.

        Note that we do not ack (acknowledge) broadcast messages so there is
        no guarantee that the message will be delivered/received.
        """
        self.tag = self.channel.basic_consume(handler, queue=self.name, no_ack=True)

    def start(self):
        """
        Starts the listener.

        This method will block until another thread calls the `stop` method.
        """
        self.channel.start_consuming()

    def stop(self):
        """
        Stops the thread and causes the `start` method to terminate.
        """
        self.logger.debug('Sending basic_cancel')
        self.channel.basic_cancel(self.tag)
        self.logger.debug('basic_cancel sent')



class MessageQueue(object):
    """
    The MessageQueue class is used for Producer/Consumer scenarios.

    Messages will be dealt out to listeners in a round-robin fashion.
    """
    def __init__(self, name, host='localhost', exchange='', durable=False, fair=False):
        self.exchange = exchange
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(name, durable=durable)
        self.tag = False
        # Set fair=True if multiple consumers are reading from a single queue.
        if fair:
            self.channel.basic_qos(prefetch_count=1)
        self.queue = name

    def publish(self, message):
        """Published the message to the queue managed by this instance."""
        self.channel.basic_publish(self.exchange, routing_key=self.queue, body=message, properties=PERSIST)

    def register(self, handler):
        """Registers the handler as a consumer for the queue managed by this instance."""
        self.tag = self.channel.basic_consume(handler, self.queue)

    def start(self):
        """Start waiting for messages to arrive on our queue."""
        self.channel.start_consuming()

    def stop(self):
        """Stop the listener and close the connection."""
        self.channel.basic_cancel(self.tag)
        self.connection.close()

    def ack(self, method):
        """Acknowledge the message."""
        self.channel.basic_ack(delivery_tag=method.delivery_tag)


class Consumer(object):
    """
    A Consumer receives messages from an input queue and "consumes" them.

    What is meant by "consume" depends on what subclasses do in their `work`
    methods.  However, Consumers do not produce "output" in the sense
    that they do not write to an output queue.
    """

    def __init__(self, name, input):
        self.name = name
        self.input_queue = MessageQueue(input)
        self.input_queue.register(handler=self._handler)
        self.listener = BroadcastListener()
        self.listener.register(handler=self._broadcast_handler)
        self.thread = False

    def _handler(self, channel, method, properties, body):
        """RabbitMQ will call the _handler method when a message arrives on the queue."""
        if body == 'HALT':
            self.stop()
            # Allow Workers to propagate the HALT message to their output_queue.
            self.halt()
        elif body == 'KILL':
            # Stops the input queue but does not propagate the messaes any further.
            self.stop()
        else:
            self.work(body)

        # Acknowledge that the message was processed.
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def _broadcast_handler(self, channel, method, properties, message):
        self.broadcast(message)

    def broadcast(self, message):
        pass

    def work(self, message):
        """Subclasses will override the work method to perform their work"""
        pass

    def halt(self):
        """Overloaded by the Worker class to propagate HALT messages."""
        print("Halting consumer " + self.name)

    def stop(self):
        self.input_queue.stop()
        self.listener.stop()

    def start(self):
        """Start listening on our input_queue.

        MessageQueues are blocking so the start() method will block until another
        process cancels the queue by sending a HALT message
        """
        print(self.name + " starting")
        # The message queues are blocking, so we need to start the broadcast
        # listener in its own thread.
        def start_listener():
            try:
                self.listener.start()
            except:
                pass
        self.input_queue.start()
        # Once the input_queue has stopped we need to wait for the listener
        # thread to terminate as well.
        self.thread.join()
        print(self.name + " halted.")


class Worker(Consumer):
    '''
    A `Worker` is a type of `Consumer` that writes its output to an
    output message queue.
    '''

    def __init__(self, name, input, output):
        super(Worker, self).__init__(name, input)
        self.output_queue = MessageQueue(output)

    def write(self, message):
        self.output_queue.publish(message)

    def halt(self):
        self.output_queue.publish('HALT')
        print("Halting worker " + self.name)


class Task(object):
    """
    The Task classes serves as the base class for services in BioASQ pipelines.

    The Task class does all the administrative busy-work needed to manage the
    RabbitMQ queues so services only need to implement the `perform` method.
    """
    def __init__(self, route):
        """Route is a String containing the unique address for the service."""
        self.bus = MessageBus()
        self.listener = BusListener(route)
        self.listener.register(self._handler)
        self.thread = False
        self.route = route
        self.logger = logging.getLogger(self.__class__.__name__)

    def start(self):
        """
        Starts the service in a separate Thread.

        The thread is started as a daemon so calls to this method don't
        block.
        """
        def run():
            try:
                self.logger.debug('Starting the listener')
                self.listener.start()
                self.logger.debug('listener.start() has exited')
            except Exception as e:
                self.logger.exception(e.message)

        t = threading.Thread(target=run)
        t.daemon = True
        t.start()
        self.thread = t

    def _handler(self, channel, method, properties, message):
        """Default message handler that calls the user's `perform` method
           and then acknowledges the message.
        """
        self.perform(message)
        self.ack(method)

    def ack(self, method):
        """Shorthand for what is otherwise a really lengthy method call."""
        self.listener.channel.basic_ack(delivery_tag=method.delivery_tag)

    def stop(self):
        """Stops the listener which will cause the `run` method above to
           exit and our thread to terminate.
        """
        self.logger.debug('Stopping the listener.')
        self.listener.stop()
        self.logger.debug('Stopped listeners.')

    def wait_for(self):
        """Waits for this task's thread to terminate."""
        self.thread.join()
        self.logger.debug('Thread %s terminated.', self.__class__.__name__)

    def perform(self, input):
        """Services should override this method to handle incoming messages."""
        pass

    def deliver(self, message):
        """Sends the message to the next target, if any."""
        target = message.forward()
        if target is not None:
            self.logger.debug('Delivering message to %s', target)
            self.bus.publish(target, Serializer.to_json(message))