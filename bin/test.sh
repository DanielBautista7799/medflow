#!/usr/bin/env bash

# MedFlow Command Center
# Day 11 - runs the complete backend test suite.

set -e

echo "== MedFlow Test Runner =="

cd backend

source .venv/bin/activate

# Check whether the local medflow_test database already exists.
DB_EXISTS=$(psql -d postgres -tAc \
    "SELECT 1 FROM pg_database WHERE datname='medflow_test'")

if [ "$DB_EXISTS" != "1" ]; then
    echo "medflow_test database not found - creating it..."

    psql -d postgres -c "CREATE DATABASE medflow_test;"
fi

echo "Running tests..."

pytest -v

echo "Test run complete."