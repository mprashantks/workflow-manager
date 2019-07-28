import pika
import time
import json
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
        self.fault_output = 'fault.out'

    @abstractmethod
    def _get_result(self, data):
        pass

    def consume(self):
        print('{0}({1}) running: [{2}]'.format(self.name, self.description, current_process()))
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = connection.channel()
        self.channel.queue_declare(queue=self.input, durable=True)
        self.channel.basic_consume(queue=self.input, on_message_callback=self.perform_operation, auto_ack=True)
        self.channel.start_consuming()

    def perform_operation(self, ch, method, properties, body):
        try:
            print('---------------')
            print('{0}({1}) performing operation: [{2}]'.format(self.name, self.description, current_process()))
            ip = json.loads(body)
            print('Input [{}]'.format(ip))
            result = self._get_result(ip)
            print('Computed result [{}]'.format(result))
            self._update_output_queue(result)
            print('---------------')
            time.sleep(self.time_limit)
        except Exception as e:
            print("caught exception %r" % e)
            self._update_fault_queue(body)

    def _update_output_queue(self, data):
        for output in self.output:
            self.channel.queue_declare(queue=output, durable=True)
            self.channel.basic_publish(exchange='', routing_key=output, body=data)

    def _update_fault_queue(self, data):
        self.channel.queue_declare(queue=self.fault_output, durable=True)
        self.channel.basic_publish(exchange='', routing_key=self.fault_output, body=data)


class TaskAdd(TaskBase):
    def __init__(self, id, name, description):
        super().__init__(
            id=id,
            name=name,
            description=description,
            parallel_limit=1,
            time_limit=1
        )

    def _get_result(self, data):
        result = data.get('n1') + data.get('n2')
        data['n1'] = result
        data['n2'] = result*2
        return json.dumps(data)


class TaskSubtract(TaskBase):
    def __init__(self, id, name, description):
        super().__init__(
            id=id,
            name=name,
            description=description,
            parallel_limit=2,
            time_limit=1
        )

    def _get_result(self, data):
        result = data.get('n1') - data.get('n2')
        data['n1'] = result
        data['n2'] = result/2
        return json.dumps(data)


class TaskProduct(TaskBase):
    def __init__(self, id, name, description):
        super().__init__(
            id=id,
            name=name,
            description=description,
            parallel_limit=2,
            time_limit=1
        )

    def _get_result(self, data):
        result = data.get('n1') * data.get('n2')
        data['n1'] = result
        data['n2'] = result+2
        return json.dumps(data)


class TaskDivision(TaskBase):
    def __init__(self, id, name, description):
        super().__init__(
            id=id,
            name=name,
            description=description,
            parallel_limit=2,
            time_limit=1
        )

    def _get_result(self, data):
        result = data.get('n1') / data.get('n2')
        data['n1'] = result
        data['n2'] = result*2
        return json.dumps(data)
