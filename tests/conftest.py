# Specify pytest plugins for other fixtures
pytest_plugins = [
    "tests.fixtures.requests",
    "tests.fixtures.clear_table_rates",
    "tests.fixtures.clear_table_event",
    "tests.fixtures.insert_test_rate",
    "tests.fixtures.insert_test_multiple_rate"
]
