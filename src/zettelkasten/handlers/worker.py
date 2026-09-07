import asyncio
from typing import Any

from zettelkasten.factories import AIProviderFactory, KnowledgeBaseClientFactory
from zettelkasten.services.notes import parse_note_job, process_note_job


def handler(event: dict[str, Any], _: Any) -> dict[str, Any]:
    """Worker Lambda: consume SQS messages, run AI + knowledge base."""
    return asyncio.run(_handle_async(event))


async def _handle_async(event: dict[str, Any]) -> dict[str, Any]:
    records = event.get("Records") or []
    batch_item_failures: list[dict[str, str]] = []

    for record in records:
        message_id = record.get("messageId") or record.get("message_id") or ""
        try:
            job = parse_note_job(record["body"])
            ai = AIProviderFactory(job.ai_provider)()
            knowledge_base = KnowledgeBaseClientFactory(job.knowledge_base)()
            await process_note_job(job, ai=ai, knowledge_base=knowledge_base)
        except Exception:
            # Report partial batch failure so only failed messages retry.
            if message_id:
                batch_item_failures.append({"itemIdentifier": message_id})
            else:
                raise

    return {"batchItemFailures": batch_item_failures}
