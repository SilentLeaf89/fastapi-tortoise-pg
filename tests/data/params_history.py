from http import HTTPStatus

test_good_get_history = [
    (
        # query
        {
            "path_calculate": "/api/v1/rate/calculate/single?date=2023-07-17&cargo_type=oil&declared_value=100000",
            "path_history": "/api/v1/history/?page_number=1&page_size=5"
        },
        # expected_answer
        {
            "status": HTTPStatus.OK,
            "len": 1
        },
        # message
        {
            "status": "Status of response is unsuccessful!",
            "len": "Body of response is unsuccessful!"
        }
    ),
]

TEST_PARAMS_HISTORY = {
    "test_good_get_history": {
        "keys": "query, expected_answer, message",
        "data": test_good_get_history,
    },
}
