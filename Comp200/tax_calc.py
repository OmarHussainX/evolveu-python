def tax(inc):
    """
    Receives one numeric parameter for income,
    Returns the amount of federal tax due
    """
    if inc > 210371:
        return .33 * (inc - 210371) + 48719
    elif inc > 147667:
        return .29 * (inc - 147667) + 30535
    elif inc > 95259:
        return .26 * (inc - 95259) + 16908
    elif inc > 47630:
        return .205 * (inc - 47630) + 7145
    else:
        return .15 * inc


def tax_recursive(inc):
    """
    Recursive tax calulation:
    Receives one numeric parameter for income,
    Returns the amount of federal tax due

    """
    if inc > 210371:
        return .33 * (inc - 210371) + tax(210371)
    elif inc > 147667:
        return .29 * (inc - 147667) + tax(147667)
    elif inc > 95259:
        return .26 * (inc - 95259) + tax(95259)
    elif inc > 47630:
        return .205 * (inc - 47630) + tax(47630)
    else:
        return .15 * inc
