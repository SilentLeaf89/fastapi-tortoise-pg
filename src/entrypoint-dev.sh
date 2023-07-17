#!/usr/bin/env bash
aerich init -t core.config.TORTOISE_ORM
aerich init-db
uvicorn main:app --host 0.0.0.0 --port 80 --reload
