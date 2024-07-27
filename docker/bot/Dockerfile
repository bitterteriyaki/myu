ARG PYTHON_VERSION=3.12.4

FROM python:${PYTHON_VERSION}-slim-bullseye AS development

# Our bot will be installed in /bot.
WORKDIR /bot

ARG BOT_ENV \
  # This is needed to fix permissions of files created in
  # the container, so that they are owned by the host user.
  UID=1000 \
  GID=1000

ENV BOT_ENV=${BOT_ENV} \
  # Python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # Pip:
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry:
  POETRY_VERSION=1.8.3 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  # Tini
  TINI_VERSION=v0.19.0 \
  # Dockerize:
  DOCKERIZE_VERSION=v0.7.0 \
  # Jishaku:
  JISHAKU_NO_UNDERSCORE=true \
  JISHAKU_NO_DM_TRACEBACK=true

# Install build dependencies.
RUN apt-get update -qq \
  && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    bash \
    curl \
    git \
  # Installing Poetry:
  && curl -sSL 'https://install.python-poetry.org' | python - \
  && poetry --version \
  # Installing Dockerize:
  && curl -sSLO "https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
  && tar -C /usr/local/bin -xzvf "dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
  && rm "dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
  && dockerize --version \
  # Installing Tini:
  && dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" \
  && curl -o /usr/local/bin/tini -sSLO "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-${dpkgArch}" \
  && chmod +x /usr/local/bin/tini \
  && tini --version \
  # Cleaning cache:
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

# We create a non-root user to run the bot,
# so that we don't run the bot as root.
RUN groupadd -g "${GID}" -r bot \
  && useradd -d '/bot' -g bot -l -r -u "${UID}" bot \
  && chown bot:bot -R '/bot'

COPY --chown=bot:bot ./poetry.lock ./pyproject.toml /bot/

RUN --mount=type=cache,target="$POETRY_CACHE_DIR" echo "${BOT_ENV}" \
  && poetry version \
  && poetry run pip install --no-deps --upgrade pip \
  && poetry install \
    $(if [ "${BOT_ENV}" = 'production' ]; then echo '--only main'; fi) \
    --no-interaction --no-ansi

USER bot


FROM development AS production

COPY --chown=bot:bot . /bot

CMD [ "python", "manage.py", "runbot" ]
