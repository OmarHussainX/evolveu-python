from read_file import read_file


def test_read_file():
    assert read_file() == 'Lines: 213, \
\'else\' statements: 3, \
characters: 9177 (8964 excluding \'\\n\')'
