import pika


def callback(ch, method, properties, body):
    if b"[Grupo]" in body:
        print(f"\n# Nova mensagem do grupo {body.decode().replace('[Grupo]', '')}")
    else:
        print(f"\n# Nova mensagem individual > {body.decode()}")


def receive_messages(channel, user):
    channel.queue_declare(queue=user)
    channel.basic_consume(queue=user, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
