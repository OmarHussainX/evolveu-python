import pytest
from tax_calc import tax, tax_recursive


# Testing non-recursive tax calculation function
def test_tax_47630():
    print(f'\nTesting non-recursive tax calculation function')
    print(f'tax on 47630: {tax(47630)}')
    assert tax(47630) == pytest.approx(7144.5, abs=0.9)


def test_tax_95259():
    print(f'tax on 95259: {tax(95259)}')
    assert tax(95259) == pytest.approx(16908.945, abs=0.9)


def test_tax_147667():
    print(f'tax on 147667: {tax(147667)}')
    assert tax(147667) == pytest.approx(30534.08, abs=0.9)


def test_tax_210371():
    print(f'tax on 210371: {tax(210371)}')
    assert tax(210371) == pytest.approx(48719.16, abs=0.9)


# Testing recursive tax calculation function
def test_tax_recursive_47630():
    print(f'\nTesting recursive tax calculation function')
    print(f'tax on 47630: {tax_recursive(47630)}')
    assert tax_recursive(47630) == pytest.approx(7144.5, abs=0.9)


def test_tax_recursive_95259():
    print(f'tax on 95259: {tax_recursive(95259)}')
    assert tax_recursive(95259) == pytest.approx(16908.945, abs=0.9)


def test_tax_recursive_147667():
    print(f'tax on 147667: {tax_recursive(147667)}')
    assert tax_recursive(147667) == pytest.approx(30534.08, abs=1)


def test_tax_recursive_210371():
    print(f'tax on 210371: {tax_recursive(210371)}')
    assert tax_recursive(210371) == pytest.approx(48719.16, abs=1)
