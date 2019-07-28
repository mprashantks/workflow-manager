import pika
import time
from multiprocessing import current_process
from abc import ABC, abstractmethod


class TaskBase(ABC):
    def __init__(self, id, name, description, parallel_limit, time_limit):
        self.id = id
        self.name = name
        self.description = description
        self.parallel_limit = parallel_limit
        self.time_limit = time_limit
        self.input = None
        self.output = []

    def consume(self, process_id):
        print('{0} is running: {1}'.format(self.name, process_id))
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue=self.input, durable=True)
        channel.basic_consume(queue=self.input, on_message_callback=self.perform_operation, auto_ack=True)

        channel.start_consuming()

    @abstractmethod
    def perform_operation(self, ch, method, properties, body):
        pass


class TaskAdd(TaskBase):
    def __init__(self, id, name, description):
        super().__init__(
            id=id,
            name=name,
            description=description,
            parallel_limit=1,
            time_limit=1
        )

    def perform_operation(self, ch, method, properties, body):
        try:
            print('{0} implementation: [{1}]'.format(self.name, current_process()))
            print("received %r" % body)
            time.sleep(self.time_limit)
        except Exception as e:
            print("caught exception %r" % e)


class TaskSubtract(TaskBase):
    def __init__(self, id, name, description):
        super().__init__(
            id=id,
            name=name,
            description=description,
            parallel_limit=2,
            time_limit=1
        )

    def perform_operation(self, ch, method, properties, body):
        try:
            print('{} implementation'.format(self.name))
            print("received %r" % body)
            time.sleep(self.time_limit)
        except Exception as e:
            print("caught exception %r" % e)


class TaskProduct(TaskBase):
    def __init__(self, id, name, description):
        super().__init__(
            id=id,
            name=name,
            description=description,
            parallel_limit=3,
            time_limit=1
        )

    def perform_operation(self, ch, method, properties, body):
        try:
            print('{} implementation'.format(self.name))
            print("received %r" % body)
            time.sleep(self.time_limit)
        except Exception as e:
            print("caught exception %r" % e)


class TaskDivision(TaskBase):
    def __init__(self, id, name, description):
        super().__init__(
            id=id,
            name=name,
            description=description,
            parallel_limit=2,
            time_limit=1
        )

    def perform_operation(self, ch, method, properties, body):
        try:
            print('{} implementation'.format(self.name))
            print("received %r" % body)
            time.sleep(self.time_limit)
        except Exception as e:
            print("caught exception %r" % e)
