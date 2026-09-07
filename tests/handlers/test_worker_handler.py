import json
from unittest.mock import AsyncMock, patch

import pytest

from zettelkasten.handlers import worker as worker_handler
from zettelkasten.models.note import Note


def _sqs_event(*bodies: str | dict, message_ids: list[str] | None = None) -> dict:
    records = []
    for index, body in enumerate(bodies):
        message_id = (
            message_ids[index]
            if message_ids is not None
            else f"msg-{index + 1}"
        )
        records.append(
            {
                "messageId": message_id,
                "body": body if isinstance(body, str) else json.dumps(body),
            }
        )
    return {"Records": records}


def _job_body(**overrides: object) -> dict:
    payload: dict = {
        "content": "Photosynthesis converts light into chemical energy.",
        "ai_provider": "mock",
        "knowledge_base": "mock",
    }
    payload.update(overrides)
    return payload


def test_worker_handler_processes_records_successfully() -> None:
    note = Note(
        title="Photosynthesis",
        content="Light to chemical energy.",
        tags=["photosynthesis"],
        external_id="mock-1",
    )
    with patch(
        "zettelkasten.handlers.worker.process_note_job",
        new_callable=AsyncMock,
        return_value=note,
    ) as process:
        result = worker_handler.handler(_sqs_event(_job_body()), None)

    assert result == {"batchItemFailures": []}
    process.assert_awaited_once()


def test_worker_handler_reports_partial_batch_failure() -> None:
    with patch(
        "zettelkasten.handlers.worker.process_note_job",
        new_callable=AsyncMock,
        side_effect=RuntimeError("boom"),
    ):
        result = worker_handler.handler(
            _sqs_event(_job_body(), message_ids=["fail-1"]),
            None,
        )

    assert result == {"batchItemFailures": [{"itemIdentifier": "fail-1"}]}


def test_worker_handler_reraises_when_message_id_missing() -> None:
    event = {
        "Records": [
            {
                "body": json.dumps(_job_body()),
            }
        ]
    }
    with (
        patch(
            "zettelkasten.handlers.worker.process_note_job",
            new_callable=AsyncMock,
            side_effect=RuntimeError("boom"),
        ),
        pytest.raises(RuntimeError, match="boom"),
    ):
        worker_handler.handler(event, None)


def test_worker_handler_invalid_job_body_is_batch_failure() -> None:
    result = worker_handler.handler(
        _sqs_event("{not-json}", message_ids=["bad-1"]),
        None,
    )

    assert result == {"batchItemFailures": [{"itemIdentifier": "bad-1"}]}


def test_worker_handler_empty_records() -> None:
    result = worker_handler.handler({"Records": []}, None)
    assert result == {"batchItemFailures": []}
