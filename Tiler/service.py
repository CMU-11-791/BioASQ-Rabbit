from deiis.rabbit import Task, Message
from deiis.model import Serializer

from Concatenation import Concatenation


if __name__ == "__main__":
    print 'Starting Tiler services.'
    task = Concatenation()
    task.start()
    task.wait_for()


