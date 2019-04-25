import pytest
from tax_calc import tax

def test_tax_47630():
    assert tax(47630) == pytest.approx(7144.5, abs=0.9)

def test_tax_95259():
    assert tax(95259) == pytest.approx(16908.945, abs=0.9)

def test_tax_147667():
    assert tax(147667) == pytest.approx(30534.08, abs=0.9)

def test_tax_210371():
    assert tax(210371) == pytest.approx(48719.16, abs=0.9)
