# syntax=docker/dockerfile:1.7@sha256:a57df69d0ea827fb7266491f2813635de6f17269be881f696fbfdf2d83dda33e
FROM python:3.11-slim-bookworm@sha256:721dc13fd1be0a771e54b72097634291d628d0007dee9da777e2ce676a9c998f AS runtime

ARG APP_UID=10001
ARG APP_GID=10001

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    XDG_CACHE_HOME=/opt/uibenchkit/cache \
    HF_HOME=/opt/uibenchkit/cache/huggingface \
    TMPDIR=/shared-tmp

RUN mkdir -p /shared-tmp \
    && apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl git tini \
    && rm -rf /var/lib/apt/lists/*

COPY docker/requirements.lock /tmp/requirements.lock
RUN python -m pip install --upgrade pip==25.3 \
    && python -m pip install \
      --extra-index-url https://download.pytorch.org/whl/cpu \
      --requirement /tmp/requirements.lock \
    && python -m playwright install --with-deps chromium \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/uibenchkit
COPY UIBenchKit/ backend/
COPY uibenchkit-cli/ cli/
RUN python -m pip install --no-deps /opt/uibenchkit/cli \
    && python -m pip check \
    && mkdir -p /opt/uibenchkit/cache /opt/uibenchkit/backend/results /shared-tmp \
    && python -c "import open_clip; open_clip.create_model_and_transforms('ViT-B-32-quickgelu', pretrained='openai')" \
    && groupadd --gid ${APP_GID} uibenchkit \
    && useradd --uid ${APP_UID} --gid ${APP_GID} --create-home uibenchkit \
    && chown -R ${APP_UID}:${APP_GID} /opt/uibenchkit /ms-playwright /shared-tmp

COPY scripts/validate_smoke.py scripts/validate_services.py /artifact/scripts/
COPY smoke-data/ /artifact/smoke-data/
RUN chown -R ${APP_UID}:${APP_GID} /artifact

USER uibenchkit
WORKDIR /opt/uibenchkit/backend
EXPOSE 5000
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "api.py", "--host", "0.0.0.0", "--port", "5000"]
