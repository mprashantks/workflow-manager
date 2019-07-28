import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='wf.test.out', durable=True)


def callback(ch, method, properties, body):
    print('Received [{}]'.format(body))


channel.basic_consume(queue='wf.test.out', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
