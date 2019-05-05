from format_email import email


def test_Larry_Shumlich():
    assert email('Larry', 'Shumlich') == 'larry.shumlich@evolveu.ca'


def test_Heiko_Peters():
    assert email('Heiko', 'Peters') == 'heiko.peters@evolveu.ca'
