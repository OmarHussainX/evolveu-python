from validate_sales_data import validate_clients


def test_validate_clients():
    assertGreaterEqual(validate_clients(), 10)
    assertLessEqual(validate_clients(), 15)
