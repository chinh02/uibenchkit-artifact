# syntax=docker/dockerfile:1.7@sha256:a57df69d0ea827fb7266491f2813635de6f17269be881f696fbfdf2d83dda33e
FROM node:22-bookworm-slim@sha256:813a7480f28fdadac1f7f5c824bcdad435b5bc1322a5968bbbdef8d058f9dff4 AS build

ENV PNPM_HOME=/pnpm
ENV PATH=${PNPM_HOME}:${PATH}
RUN corepack enable && corepack prepare pnpm@10.14.0 --activate

WORKDIR /build
COPY uibenchkit-GUI/package.json uibenchkit-GUI/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY uibenchkit-GUI/ ./
RUN pnpm build

FROM node:22-bookworm-slim@sha256:813a7480f28fdadac1f7f5c824bcdad435b5bc1322a5968bbbdef8d058f9dff4 AS runtime

ARG APP_UID=10001
ARG APP_GID=10001

ENV PNPM_HOME=/pnpm \
    PATH=/pnpm:${PATH} \
    NODE_ENV=production \
    PORT=3000 \
    TMPDIR=/shared-tmp

RUN corepack enable \
    && corepack prepare pnpm@10.14.0 --activate \
    && groupadd --gid ${APP_GID} uibenchkit \
    && useradd --uid ${APP_UID} --gid ${APP_GID} --create-home uibenchkit \
    && mkdir -p /app /shared-tmp /opt/uibenchkit/backend/results \
    && chown -R ${APP_UID}:${APP_GID} /app /shared-tmp /opt/uibenchkit

WORKDIR /app
COPY --from=build /build/package.json /build/pnpm-lock.yaml ./
RUN pnpm install --prod --frozen-lockfile
COPY --from=build /build/dist/ ./dist/

USER uibenchkit
EXPOSE 3000
CMD ["node", "dist/server/node-build.mjs"]
