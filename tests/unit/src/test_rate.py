import pytest

from tests.data.params_rate import TEST_PARAMS_RATE


@pytest.mark.parametrize(
    TEST_PARAMS_RATE["test_good_single_add"]["keys"],
    TEST_PARAMS_RATE["test_good_single_add"]["data"],
)
async def test_good_single_add(
        make_post_request,
        clear_table_rates,
        query,
        expected_answer,
        message
        ):
    # Request data
    _, status = await make_post_request(
        path=query["path"], query_data=query["data"]
    )
    # Check the response
    assert status == expected_answer["status"], message["status"]
    await clear_table_rates()


@pytest.mark.parametrize(
    TEST_PARAMS_RATE["test_good_multiple_add"]["keys"],
    TEST_PARAMS_RATE["test_good_multiple_add"]["data"],
)
async def test_good_multiple_add(
    make_post_request,
    clear_table_rates,
    query,
    expected_answer,
    message,
):

    # Request data
    _, status = await make_post_request(
        path=query["path"], query_data=query["data"])
    # Check the response
    assert status == expected_answer["status"], message["status"]
    await clear_table_rates()


@pytest.mark.parametrize(
    TEST_PARAMS_RATE["test_good_get_all_rates"]["keys"],
    TEST_PARAMS_RATE["test_good_get_all_rates"]["data"],
)
async def test_good_get_all_rates(
    make_get_request,
    insert_test_rate,
    clear_table_rates,
    query,
    expected_answer,
    message,
):
    await insert_test_rate()

    # Request all rates
    _, status = await make_get_request(path=query["path"])

    assert status == expected_answer["status"], message["status"]

    await clear_table_rates()


@pytest.mark.parametrize(
    TEST_PARAMS_RATE["test_good_get_rate"]["keys"],
    TEST_PARAMS_RATE["test_good_get_rate"]["data"],
)
async def test_good_get_rate(
    make_get_request,
    insert_test_rate,
    clear_table_rates,
    query,
    expected_answer,
    message,
):
    # add rate
    await insert_test_rate()

    # get rate
    _, status = await make_get_request(path=query["path"])

    assert status == expected_answer["status"], message["status"]

    await clear_table_rates()


@pytest.mark.parametrize(
    TEST_PARAMS_RATE["test_good_change"]["keys"],
    TEST_PARAMS_RATE["test_good_change"]["data"],
)
async def test_good_change(
    make_put_request,
    insert_test_rate,
    clear_table_rates,
    query,
    expected_answer,
    message,
):
    # add rate
    await insert_test_rate()

    # Request change
    body_change, status = await make_put_request(
        path=query["path_change"],
        query_data=query["data_change"],
    )

    assert status == expected_answer["status"], message["status"]
    assert body_change["rate"] == expected_answer["rate"], message["rate"]

    await clear_table_rates()


@pytest.mark.parametrize(
    TEST_PARAMS_RATE["test_good_delete"]["keys"],
    TEST_PARAMS_RATE["test_good_delete"]["data"],
)
async def test_good_delete(
    make_delete_request,
    insert_test_rate,
    clear_table_rates,
    query,
    expected_answer,
    message,
):
    # add rate
    await insert_test_rate()

    # Request delete
    _, status = await make_delete_request(
        path=query["path_delete"]
    )

    assert status == expected_answer["status"], message["status"]

    await clear_table_rates()


@pytest.mark.parametrize(
    TEST_PARAMS_RATE["test_good_calculate_single"]["keys"],
    TEST_PARAMS_RATE["test_good_calculate_single"]["data"],
)
async def test_good_calculate_single(
    make_get_request,
    insert_test_rate,
    clear_table_rates,
    query,
    expected_answer,
    message,
):
    # add rate
    await insert_test_rate()

    # Request calculate
    body, status = await make_get_request(path=query["path"])

    assert status == expected_answer["status"], message["status"]
    assert body == expected_answer["body"], message["status"]

    await clear_table_rates()


@pytest.mark.parametrize(
    TEST_PARAMS_RATE["test_good_calculate_multiple"]["keys"],
    TEST_PARAMS_RATE["test_good_calculate_multiple"]["data"],
)
async def test_good_calculate_multiple(
    make_post_request,
    insert_test_multiple_rate,
    clear_table_rates,
    query,
    expected_answer,
    message,
):
    # add rates
    await insert_test_multiple_rate()

    # Request data
    body, status = await make_post_request(
        path=query["path"], query_data=query["data"])

    # Check the response
    assert status == expected_answer["status"], message["status"]
    assert body == expected_answer["body"], message["status"]

    await clear_table_rates()
