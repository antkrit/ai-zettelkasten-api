from zettelkasten.clients.sqs import SQSClient
from zettelkasten.config import settings
from zettelkasten.models.job import NoteJob


def enqueue_note_job(job: NoteJob) -> str:
    """Put a note job on SQS; returns the SQS MessageId."""
    if not settings.aws.notes_queue_url:
        raise ValueError("AWS_NOTES_QUEUE_URL is required to enqueue jobs")

    sqs_client = SQSClient(region=settings.aws.region or None)
    response = sqs_client.send_message(
        QueueUrl=settings.aws.notes_queue_url,
        MessageBody=job.model_dump_json(),
    )
    message_id = response.get("MessageId")
    if not isinstance(message_id, str):
        raise TypeError(f"Unexpected SQS MessageId: {message_id!r}")
    return message_id
