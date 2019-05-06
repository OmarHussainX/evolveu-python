from validate_sales_data import validate_sales_data


def test_validate_good_data():
    assert(validate_sales_data('sales_data.xlsx'))


def test_insufficient_clients():
    assert not (validate_sales_data('sales_data_bad1.xlsx'))


def test_too_many_clients():
    assert not (validate_sales_data('sales_data_bad2.xlsx'))


def test_repeated_clients():
    assert not (validate_sales_data('sales_data_bad3.xlsx'))


def test_too_few_invoices_per_client():
    assert not (validate_sales_data('sales_data_bad4.xlsx'))


def test_too_many_invoices_per_client():
    assert not (validate_sales_data('sales_data_bad5.xlsx'))


def test_invoices_not_in_same_month():
    assert not (validate_sales_data('sales_data_bad6.xlsx'))


def test_invoices_total_low():
    assert not (validate_sales_data('sales_data_bad7.xlsx'))


def test_invoices_total_high():
    assert not (validate_sales_data('sales_data_bad8.xlsx'))
