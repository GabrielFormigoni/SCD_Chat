import pika


def create_group_exchange(channel, group_name):
    channel.exchange_declare(exchange=group_name, exchange_type="fanout")
    print(f"Exchange do grupo '{group_name}' criada.")
