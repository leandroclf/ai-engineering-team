# Provider CLI runtime: the container is the sandbox (host bwrap is unavailable).
FROM node:22-bookworm-slim
ARG CODEX_VERSION=0.159.3
ARG CLAUDE_VERSION=2.1.287
ARG UID=1001
RUN apt-get update \
 && apt-get install -y --no-install-recommends git python3 python3-yaml ripgrep ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && npm install -g @openai/codex@${CODEX_VERSION} @anthropic-ai/claude-code@${CLAUDE_VERSION} \
 && npm cache clean --force \
 && userdel -r node \
 && useradd -m -u ${UID} -s /bin/bash agent
USER agent
WORKDIR /work
