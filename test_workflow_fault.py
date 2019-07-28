import pika


# RabbitMQ channel
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Fault information
channel.queue_declare(queue='fault.out', durable=True)


def callback(ch, method, properties, body):
    print('Received [{}]'.format(body))


print('Test workflow fault')
channel.basic_consume(queue='fault.out', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
