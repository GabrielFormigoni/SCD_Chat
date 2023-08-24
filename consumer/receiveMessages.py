import pika


def callback(ch, method, properties, body):
    if b"[Grupo]" in body:
        print(f"Nova mensagem de grupo: {body.decode().replace('[Grupo]', '')}")
    else:
        print(f"Nova mensagem individual: {body.decode()}")


def receive_messages(channel, user):
    channel.queue_declare(queue=user)
    channel.basic_consume(queue=user, on_message_callback=callback, auto_ack=True)
    print(f"Recebendo mensagens para {user}. Pressione CTRL+C para sair.")
    channel.start_consuming()
