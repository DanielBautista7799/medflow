#!/usr/bin/env bash

# MedFlow Command Center
# Day 11 - seeds MedFlow data in the correct order.
#
# Run:
# bash bin/seed.sh local
# bash bin/seed.sh rds

set -e

# $1 is the first argument after the script name.
# If no argument is given, use "local".
TARGET="${1:-local}"

if [ "$TARGET" = "local" ]; then

    export DATABASE_URL="postgresql+asyncpg://danielbautista@127.0.0.1:5432/medflow_dev"

    PSQL_HOST="127.0.0.1"
    PSQL_USER="danielbautista"
    PSQL_DB="medflow_dev"

elif [ "$TARGET" = "rds" ]; then

    # Replace these values only when intentionally seeding RDS.
    export DATABASE_URL="postgresql+asyncpg://postgres:<RDS_PASSWORD>@<RDS_ENDPOINT>:5432/medflow"

    PSQL_HOST="<RDS_ENDPOINT>"
    PSQL_USER="postgres"
    PSQL_DB="medflow"

else

    echo "Usage: bash bin/seed.sh [local|rds]"
    exit 1

fi

echo "Seeding target: $TARGET"

cd backend

echo "Creating database tables..."
python -m scripts.day3_create_tables

echo "Loading business data..."
psql \
    -h "$PSQL_HOST" \
    -U "$PSQL_USER" \
    -d "$PSQL_DB" \
    -f db/sql/seed.sql

echo "Creating RBAC users..."
python -m scripts.day5_seed_users

echo "Seed complete for $TARGET."