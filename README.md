# AI Zettelkasten

Serverless note pipeline: API Lambda enqueues jobs to SQS; worker Lambda runs AI + Knowledge base.

## Development

```bash
uv sync --group dev
uv run pre-commit install
```

Hooks run Ruff (lint + format) and `ty` on commit. Run manually with `uv run pre-commit run --all-files`.

## Local handler testing

Handlers are normal functions: `handler(event, context)`. Call them from a Python one-liner or REPL; no HTTP server.
