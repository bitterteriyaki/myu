#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

readonly cmd="$*"

export DATABASE_URL="postgresql+asyncpg://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB"

wait-for-it \
  --host="$POSTGRES_HOST" \
  --port="$POSTGRES_PORT" \
  --timeout=90 \
  --strict

echo "PostgreSQL is up. Continuing..."

# Apply database migrations
# alembic upgrade head

# Evaluating passed command (do not touch):
exec $cmd
