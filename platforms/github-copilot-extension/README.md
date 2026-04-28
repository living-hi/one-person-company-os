# GitHub Copilot Extension Draft

This adapter is a marketplace planning package for a future GitHub Copilot Extension.

Copilot Extensions require:

- a GitHub App
- a public webhook/API backend
- Marketplace publisher approval
- an endpoint that converts Copilot chat requests into backend actions

Recommended backend:

- expose the same operations as `platforms/openai-gpt/actions-openapi.yaml`
- enforce workspace approval and path boundaries
- return generated cockpit summaries as Markdown

Do not submit this adapter as a complete extension until a hosted backend exists.
