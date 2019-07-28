import pika


# RabbitMQ channel
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# One workflow output queue
channel.queue_declare(queue='wf.test.out.1', durable=True)


def callback(ch, method, properties, body):
    print('Received [{}]'.format(body))


print('Test workflow output')
channel.basic_consume(queue='wf.test.out.1', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
