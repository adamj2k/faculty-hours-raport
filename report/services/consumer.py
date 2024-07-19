import pika
import pika.adapters.asyncio_connection
from aio_pika import IncomingMessage, connect_robust

from report.logic.generate_reports import (
    generate_personal_workload_reports,
    generate_summary_reports,
    generate_teachers_reports,
)
from report.logic.save_reports import (
    save_personal_workload_report,
    save_summary_report,
    save_teachers_report,
)
from report.settings import RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_USER
from report.utils.utils import find_teacher_id_in_body


async def callback_teacher_report(message: IncomingMessage):
    await message.ack()
    body = message.body.decode("utf-8")
    report = generate_teachers_reports()
    save_teachers_report(report)
    print(f"{body} report is saved")


async def callback_personal_report(message: IncomingMessage):
    await message.ack()
    body = message.body.decode("utf-8")
    teacher_id = find_teacher_id_in_body(str(body))
    if not teacher_id:
        print(f"{body} not saved")
        return
    else:
        report = generate_personal_workload_reports(teacher_id)
        save_personal_workload_report(report)
        print(f"{body} saved")


# TODO : change callback function to async with fix of generation summary report function
def callback_summary_report(ch, method, properties, body):
    print(f"Making {body}")
    report = generate_summary_reports()
    save_summary_report(report)
    print(f"{body} saved")
    ch.basic_ack(delivery_tag=method.delivery_tag)


QUEUE_CALLBACK = {
    "teacher-report-queue": callback_teacher_report,
    "personal-report-queue": callback_personal_report,
    "summary-report-queue": callback_summary_report,
}


class PikaConsumer:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                RABBITMQ_HOST,
                5672,
                "faculty-vhost",
                pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD),
            )
        )
        self.channel = self.connection.channel()
        for index, (queue, callback) in enumerate(QUEUE_CALLBACK.items()):
            self.channel.queue_declare(queue=queue, durable=True)

    async def consume(self, loop):
        connection = await connect_robust(
            host=RABBITMQ_HOST,
            virtualhost="faculty-vhost",
            port=5672,
            loop=loop,
            login=RABBITMQ_USER,
            password=RABBITMQ_PASSWORD,
        )
        channel = await connection.channel()

        for index, (queue, callback) in enumerate(QUEUE_CALLBACK.items()):
            queue_connection = await channel.declare_queue(queue, durable=True)
            await queue_connection.consume(callback, no_ack=False)

        return connection
