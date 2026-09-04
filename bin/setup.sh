#!/usr/bin/env bash

# MedFlow Command Center
# Day 11 - sets up a fresh clone of the project.

set -e

echo "== MedFlow Setup =="

cd backend

# Create the virtual environment if it does not already exist.
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate the backend virtual environment.
source .venv/bin/activate

echo "Installing backend dependencies..."
pip install -r requirements.txt

# Create the real .env from the safe template if one does not exist.
if [ ! -f ".env" ]; then
    echo "No .env found - copying from .env.example."
    echo "Fill in real values in backend/.env before running the app."
    cp .env.example .env
fi

# Install frontend dependencies.
cd ../frontend

echo "Installing frontend dependencies..."
npm install

echo "Setup complete."