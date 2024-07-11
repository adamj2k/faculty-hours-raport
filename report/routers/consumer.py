import pika

from report.routers.generate_reports import (
    generate_personal_workload_reports,
    generate_summary_reports,
    generate_teachers_reports,
)
from report.routers.save_reports import (
    save_personal_workload_report,
    save_summary_report,
    save_teachers_report,
)
from report.settings import RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_USER

QUEUE_CALLBACK = {
    "teacher-report-queue": "callback_teacher_report",
    "personal-report-queue": "callback_personal_report",
    "summary-report-queue": "callback_summary_report",
}


def callback_teacher_report(ch, method, properties, body):
    print(f"Making {body}")
    report = generate_teachers_reports()
    save_teachers_report(report)
    print(f"{body} saved")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def callback_personal_report(ch, method, properties, body):
    print(f"Making {body}")
    report = generate_personal_workload_reports()
    save_personal_workload_report(report)
    print(f"{body} saved")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def callback_summary_report(ch, method, properties, body):
    print(f"Making {body}")
    report = generate_summary_reports()
    save_summary_report(report)
    print(f"{body} saved")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consumer():
    """
    Consuming messages from each queue in list QUEUE
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            RABBITMQ_HOST,
            5672,
            "/",
            pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD),
        )
    )
    channel = connection.channel()

    for index, (queue, callback) in enumerate(QUEUE_CALLBACK.items()):
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
