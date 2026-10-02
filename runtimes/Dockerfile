# Provider CLI runtime: the container is the sandbox (host bwrap is unavailable).
FROM node:22-bookworm-slim
ARG CODEX_VERSION=0.159.3
ARG CLAUDE_VERSION=2.1.287
ARG UID=1001
COPY requirements-validation.txt /tmp/requirements-validation.txt
RUN apt-get update \
 && apt-get install -y --no-install-recommends git python3 python3-venv ripgrep ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && python3 -m venv /opt/validation \
 && /opt/validation/bin/pip install --no-cache-dir -r /tmp/requirements-validation.txt \
 && npm install -g @openai/codex@${CODEX_VERSION} @anthropic-ai/claude-code@${CLAUDE_VERSION} \
 && npm cache clean --force \
 && userdel -r node \
 && useradd -m -u ${UID} -s /bin/bash agent
ENV PATH="/opt/validation/bin:${PATH}"
USER agent
WORKDIR /work
