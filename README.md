# AI Zettelkasten

Serverless note pipeline: API Lambda enqueues jobs to SQS; worker Lambda runs AI + Knowledge base.

## Local handler testing

Handlers are normal functions: `handler(event, context)`. Call them from a Python one-liner or REPL; no HTTP server.
