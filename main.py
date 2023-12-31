import pika
import threading
from producer.sendMessages import send_message
from producer.createGroup import create_group_exchange
from consumer.receiveMessages import receive_messages


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    user = input("Digite seu nome de usuário: ")
    group_name = ""

    def start_message_consumption(user):
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
        receive_messages(channel, user)
        connection.close()

    message_thread = threading.Thread(target=start_message_consumption, args=(user,))
    message_thread.start()

    try:
        while True:
            print("\nEscolha uma operação:")
            print("1. Criar grupo")
            print("2. Adicionar pessoa ao grupo")
            print("3. Enviar mensagem para alguém")
            print("4. Enviar mensagem para grupo")
            print("5. Sair")

            choice = input("Digite o número da operação desejada: ")

            if choice == "1":
                group_name = input("Digite o nome do grupo: ")
                create_group_exchange(channel, group_name)
                print(f"# Grupo '{group_name}' criado.")
            elif choice == "2":
                group_name = input(
                    "Digite o nome do grupo a ser adicionado o novo usuário: "
                )
                user_to_add = input("Digite o nome do usuário a ser adicionado: ")
                channel.queue_declare(queue=user_to_add)
                channel.queue_bind(exchange=group_name, queue=user_to_add)
                print(f"# {user_to_add} adicionado ao grupo '{group_name}'.")
            elif choice == "3":
                recipient = input("Digite o destinatário da mensagem: ")
                message = input("Digite a mensagem: ")
                send_message(channel, recipient, f"{user}: {message}")
            elif choice == "4":
                group_name = input(
                    "Digite o nome do grupo para o qual deseja enviar a mensagem: "
                )
                message = input(f"Digite a mensagem para enviar ao grupo '{group_name}': ")
                send_message(
                    channel,
                    group_name,
                    f"{user}: {message}",
                    is_group=True,
                    group_name=group_name,
                )
            elif choice == "5":
                break
            else:
                print("Opção inválida. Escolha uma opção válida.")
    except KeyboardInterrupt:
        connection.close()

    connection.close()


if __name__ == "__main__":
    main()