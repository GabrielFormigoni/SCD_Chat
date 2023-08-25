import pika


def send_message(channel, recipient, message, is_group=False, group_name=None):
    if is_group:
        if group_name:
            channel.basic_publish(
                exchange=group_name, routing_key="", body=f"[Grupo]'{group_name}' > {message}"
            )
            print(f"# Mensagem enviada para o grupo '{group_name}'.")
        else:
            print("# Nome do grupo não fornecido. Mensagem não enviada.")
    else:
        channel.basic_publish(exchange="", routing_key=recipient, body=message)
        print(f"# Mensagem enviada para {recipient}.")
