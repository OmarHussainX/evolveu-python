def email(first, last):
    """
    Receives two string parameters for first & last name,
    Returns an all-lowercase 'first.last@evolveu.ca' email address
    """
    return f'{first.lower()}.{last.lower()}@evolveu.ca'
