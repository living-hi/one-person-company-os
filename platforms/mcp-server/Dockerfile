FROM python:3.11-slim

LABEL org.opencontainers.image.title="One Person Company OS MCP Server"
LABEL org.opencontainers.image.description="Stdio MCP adapter for One Person Company OS."
LABEL org.opencontainers.image.source="https://github.com/living-hi/one-person-company-os"
LABEL org.opencontainers.image.licenses="MIT-0"
LABEL io.modelcontextprotocol.server.name="io.github.living-hi/one-person-company-os"

WORKDIR /app
COPY . /app

ENTRYPOINT ["python3", "platforms/mcp-server/server.py"]
