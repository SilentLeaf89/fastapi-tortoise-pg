#!/usr/bin/env bash
pip install -r /tests/test_requirements.txt
pytest /tests/unit/src --durations=3 > /tests/logs/pytest.output.log
