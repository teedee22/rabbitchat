import pika
import json

name = input("Enter your chat name: ")

def connect(name):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', client_properties={
            'connection_name': name
        }))
    channel = connection.channel()

    channel.queue_declare(queue=name, auto_delete=True)
    channel.exchange_declare(exchange='private', exchange_type='fanout', auto_delete=True)
    channel.queue_bind(name, 'private')
    return connection, channel

while True:
    try:
        message = input(f"\033[1m{name} \033[0m: ")
        payload = json.dumps({'name': name, 'message': message})
        connection, channel = connect(name)
        channel.basic_publish(exchange='private', routing_key="", body=payload)
        connection.close()
    except KeyboardInterrupt:
        print("\n Connection closed")
        break

