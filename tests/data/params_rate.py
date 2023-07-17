from http import HTTPStatus

test_good_single_add = [
    (
        # query
        {
            "path": "/api/v1/rate/add/single",
            "data": {
                "date": "2023-07-17",
                "cargo_type": "test",
                "rate": 0.001
            }
        },
        # expected_answer
        {"status": HTTPStatus.OK},
        # message
        {
            "status": "Status of response is unsuccessful!",
        },
    ),
]

test_good_multiple_add = [
    (
        # query
        {
            "path": "/api/v1/rate/add/multiple",
            "data": {
                "2023-07-15": [{"cargo_type": "Wood", "rate": 0.001}],
                "2023-07-16": [{"cargo_type": "Steel", "rate": 0.003},
                               {"cargo_type": "Cooper", "rate": 0.002}],
                "2023-07-17": [{"cargo_type": "Chocolate", "rate": 0.005}]
            }
        },
        # expected_answer
        {"status": HTTPStatus.OK},
        # message
        {"status": "Status of response is unsuccessful!"},
    ),
]

test_good_get_all_rates = [
    (
        # query
        {"path": "/api/v1/rate/"},
        # expected_answer
        {"status": HTTPStatus.OK},
        # message
        {"status": "Status of response is unsuccessful!"}
    ),
]

test_good_get_rate = [
    (
        # query
        {"path": "/api/v1/rate/c2b9c859-9803-4d60-9a06-956f33ffec47"},
        # expected_answer
        {"status": HTTPStatus.OK},
        # message
        {"status": "Status of response is unsuccessful!"}
    ),
]

test_good_change = [
    (
        # query
        {
            "path_change": "/api/v1/rate/c2b9c859-9803-4d60-9a06-956f33ffec47",
            "data_change": {"date": "2022-07-17",
                            "cargo_type": "string",
                            "rate": 0.01
                            }
        },
        # expected_answer
        {
            "status": HTTPStatus.OK,
            "rate": 0.01,
        },
        # message
        {
            "status": "Changes failed",
            "rate": "Rate not changed"
        }
    ),
]

test_good_delete = [
    (
        # query
        {
            "path_delete": "/api/v1/rate/c2b9c859-9803-4d60-9a06-956f33ffec47",
        },
        # expected_answer
        {"status": HTTPStatus.OK},
        # message
        {"status": "Status of response is unsuccessful!"}
    ),
]

test_good_calculate_single = [
    (
        # query
        {"path": "/api/v1/rate/calculate/single?date=2023-07-17&cargo_type=oil&declared_value=100000"},
        # expected_answer
        {
            "status": HTTPStatus.OK,
            "body": {"cost_of_insurance": 100}
        },
        # message
        {
            "status": "Status of response is unsuccessful!",
            "body": "The cost of insurance is calculated incorrectly"
        }
    ),
]

test_good_calculate_multiple = [
    (
        # query
        {
            "path": "/api/v1/rate/calculate/multiple",
            "data": {
                "2023-07-15": [{"cargo_type": "Wood", "declared_value": 1000000}],
                "2023-07-16": [{"cargo_type": "Steel", "declared_value": 1000000},
                               {"cargo_type": "Cooper", "declared_value": 1000000}],
                "2023-07-17": [{"cargo_type": "Chocolate", "declared_value": 1000000}]
            }
        },
        # expected_answer
        {
            "status": HTTPStatus.OK,
            "body": {"total_cost": 11000.0}
        },
        # message
        {
            "status": "Status of response is unsuccessful!",
            "body": "The cost of insurance is calculated incorrectly"
         },
    ),
]

TEST_PARAMS_RATE = {
    "test_good_single_add": {
        "keys": "query, expected_answer, message",
        "data": test_good_single_add,
    },
    "test_good_multiple_add": {
        "keys": "query, expected_answer, message",
        "data": test_good_multiple_add,
    },
    "test_good_get_all_rates": {
        "keys": "query, expected_answer, message",
        "data": test_good_get_all_rates,
    },
    "test_good_get_rate": {
        "keys": "query, expected_answer, message",
        "data": test_good_get_rate,
    },
    "test_good_change": {
        "keys": "query, expected_answer, message",
        "data": test_good_change,
    },
    "test_good_delete": {
        "keys": "query, expected_answer, message",
        "data": test_good_delete,
    },
    "test_good_calculate_single": {
        "keys": "query, expected_answer, message",
        "data": test_good_calculate_single,
    },
    "test_good_calculate_multiple": {
        "keys": "query, expected_answer, message",
        "data": test_good_calculate_multiple,
    },
}
