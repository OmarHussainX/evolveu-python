from validate_sales_data import validate_sales_data


def test_validate_good_data():
    assert(validate_sales_data('sales_data.xlsx'))


def test_invalidate_bad_data():
    assert not (validate_sales_data('sales_data_bad.xlsx'))
