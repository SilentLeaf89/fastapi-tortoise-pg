import pytest

from tests.data.params_history import TEST_PARAMS_HISTORY


@pytest.mark.parametrize(
    TEST_PARAMS_HISTORY["test_good_get_history"]["keys"],
    TEST_PARAMS_HISTORY["test_good_get_history"]["data"],
)
async def test_good_get_history(
    insert_test_rate,
    make_get_request,
    clear_table_event,
    clear_table_rates,
    query,
    expected_answer,
    message,
):
    # add rate
    await insert_test_rate()

    # Request calculate
    _, _ = await make_get_request(path=query["path_calculate"])

    body, status = await make_get_request(path=query["path_history"])

    assert len(body) == expected_answer["len"], message["len"]
    assert status == expected_answer["status"], message["status"]

    await clear_table_event()
    await clear_table_rates()
