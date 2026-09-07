import base64
import json
from typing import Any

from zettelkasten.models.job import NoteJob
from zettelkasten.services.sqs import enqueue_note_job


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """API Lambda: validate request, enqueue SQS job, return 202."""
    try:
        job = NoteJob.model_validate(_extract_json_body(event))
        message_id = enqueue_note_job(job)
    except Exception as exc:
        return _response(400, {"error": str(exc)})

    return _response(202, {"status": "accepted", "message_id": message_id})


def _extract_json_body(event: dict[str, Any]) -> Any:
    # Lambda Function URL / API Gateway-style event
    if "body" in event:
        body = event.get("body") or "{}"
        if event.get("isBase64Encoded"):
            body = base64.b64decode(body).decode("utf-8")
        if isinstance(body, (bytes, bytearray)):
            body = body.decode("utf-8")
        return json.loads(body) if isinstance(body, str) else body

    # Direct invoke with the job payload
    return event


def _response(status_code: int, body: dict[str, Any]) -> dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }
