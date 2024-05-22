import json
import pika
from datetime import datetime
import logging.config

from actions import SendMail, logger, error_cooldown
from exceptions import ConnectException
import settings


def set_logging():
    logging.config.dictConfig(settings.LOGGING)

def connect_rabbitmq(): 
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT)
    )
    channel = connection.channel()
    channel.queue_declare(queue=settings.RABBITMQ_MAIL_MESSAGE_QUEUE, durable=True)
    return channel
  
def callback_message(ch, method, properties, body):
    body = json.loads(body.decode())
    logger("info", " [v] Received %s" % body.get('recipients'))
    send_mail = SendMail(body.get("recipients"), body.get("user_id"))
    try:
        send_result = send_mail(body.get("subject", "ZeroOne"), body.get("message"))
        if send_result["status"] is True:
            logger("info", " [v] Done ")
        else:
            logger("error", " [x] Error: %s" % send_result["message"])

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except ConnectException as e:
        logger("critical", e)

        ch.basic_nack(delivery_tag=method.delivery_tag)
        
        error_cooldown()

def main():
    set_logging()
    logger("info", " Start time: %s" % datetime.now())
    logger("info", f" [*] Connection to RabbitMQ: host={settings.RABBITMQ_HOST}, " \
                   f"port={settings.RABBITMQ_PORT}, queue={settings.RABBITMQ_MAIL_MESSAGE_QUEUE}")
    channel = connect_rabbitmq()
    logger("info", " [*] Waiting for messages.")
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=settings.RABBITMQ_MAIL_MESSAGE_QUEUE, on_message_callback=callback_message)
    channel.start_consuming()

if __name__ == '__main__':
    main()  
