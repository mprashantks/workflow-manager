import pika
import time
import random
import json


# RabbitMQ channel
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Workflow input queue
channel.queue_declare(queue='wf.test.in', durable=True)

for i in range(10):

    # Test with good input and bad input
    # Good input consists of two numbers, n1 and n2 (Will be processed correctly)
    # Bad input consists of only single number (Will throw an exception)
    choice = [
        {
            'id': i,
            'n1': random.randint(1, 100),
            'n2': random.randint(1, 100)
        },
        {
            'id': i,
            'n1': random.randint(1, 100),
            'n2': random.randint(1, 100)
        },
        {
            'id': i,
            'n1': random.randint(1, 100),
            'n2': random.randint(1, 100)
        },
        {
            'id': i,
            'n1': random.randint(1, 100)
        }
    ]

    msg = json.dumps(random.choice(choice))
    channel.basic_publish(exchange='', routing_key='wf.test.in', body=msg)
    print(msg)
    time.sleep(1)

# connection.close()
