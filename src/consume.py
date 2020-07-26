import pika
import json

name = input("Enter your chat name: ")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', client_properties={
        'connection_name': f"{name} : hermes"
    }))
channel = connection.channel()

channel.queue_declare(queue=name, auto_delete=True)
channel.exchange_declare(exchange='private', exchange_type='fanout', auto_delete=True)
channel.queue_bind(name, 'private')

def callback(ch, method, properties, body):
    payload = json.loads(body)
    print(f"\033[1m{payload['name']} \033[0m: {payload['message']} ")


channel.basic_consume(
    queue=name, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\n Connection closed")
    connection.close()