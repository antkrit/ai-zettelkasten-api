from typing import Any

import boto3


class SQSClient:
    """Thin proxy around boto3's SQS client (`SQSClient().x` → `_client.x`)."""

    def __init__(self, *, region: str | None = None) -> None:
        kwargs: dict[str, Any] = {}
        if region:
            kwargs["region_name"] = region
        self._client = boto3.client("sqs", **kwargs)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._client, name)
