import base64
import json
from unittest.mock import patch

from zettelkasten.handlers import api as api_handler
from zettelkasten.models.job import NoteJob


def _job_payload(**overrides: object) -> dict:
    payload: dict = {
        "content": "Photosynthesis converts light into chemical energy.",
        "ai_provider": "mock",
        "knowledge_base": "mock",
    }
    payload.update(overrides)
    return payload


def test_api_handler_direct_invoke_returns_202() -> None:
    with patch(
        "zettelkasten.handlers.api.enqueue_note_job",
        return_value="msg-123",
    ) as enqueue:
        result = api_handler.handler(_job_payload(), None)

    assert result["statusCode"] == 202
    assert result["headers"]["Content-Type"] == "application/json"
    body = json.loads(result["body"])
    assert body == {"status": "accepted", "message_id": "msg-123"}
    enqueue.assert_called_once()
    job = enqueue.call_args.args[0]
    assert isinstance(job, NoteJob)
    assert job.content.startswith("Photosynthesis")


def test_api_handler_function_url_body_returns_202() -> None:
    event = {"body": json.dumps(_job_payload())}
    with patch(
        "zettelkasten.handlers.api.enqueue_note_job",
        return_value="msg-456",
    ):
        result = api_handler.handler(event, None)

    assert result["statusCode"] == 202
    assert json.loads(result["body"])["message_id"] == "msg-456"


def test_api_handler_base64_body_returns_202() -> None:
    raw = json.dumps(_job_payload()).encode("utf-8")
    event = {
        "body": base64.b64encode(raw).decode("ascii"),
        "isBase64Encoded": True,
    }
    with patch(
        "zettelkasten.handlers.api.enqueue_note_job",
        return_value="msg-789",
    ):
        result = api_handler.handler(event, None)

    assert result["statusCode"] == 202
    assert json.loads(result["body"])["message_id"] == "msg-789"


def test_api_handler_invalid_payload_returns_400() -> None:
    result = api_handler.handler({"content": ""}, None)

    assert result["statusCode"] == 400
    body = json.loads(result["body"])
    assert "error" in body


def test_api_handler_enqueue_failure_returns_400() -> None:
    with patch(
        "zettelkasten.handlers.api.enqueue_note_job",
        side_effect=ValueError("AWS_NOTES_QUEUE_URL is required to enqueue jobs"),
    ):
        result = api_handler.handler(_job_payload(), None)

    assert result["statusCode"] == 400
    assert "AWS_NOTES_QUEUE_URL" in json.loads(result["body"])["error"]
