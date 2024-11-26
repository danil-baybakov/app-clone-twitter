#!/bin/bash

alembic upgrade head

# shellcheck disable=SC2164
cd app

uvicorn main:app --host 0.0.0.0 --port 5000 --reload;