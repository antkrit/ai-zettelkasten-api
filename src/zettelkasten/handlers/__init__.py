"""AWS Lambda entrypoints."""

from zettelkasten.handlers.api import handler as api_handler
from zettelkasten.handlers.worker import handler as worker_handler

__all__ = ["api_handler", "worker_handler"]
