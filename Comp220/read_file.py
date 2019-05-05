def read_file():
    """
    Reads file 'syntax.html' from the current directory, and returns a string:
    "Lines: ##, 'else' statements: ##, characters: ## (## excluding '\n')"
    """
    # open file _with_ promise to close as soon as code block has executed
    with open('syntax.html', 'r') as f:
        file_lines = f.readlines()  # list(f) also works
        char_count = 0
        newline_count = 0
        else_count = 0

        # Loop through the lines, and for every line...
        #  - add its length (less 1 for '\n') to char_count
        #    (Actually, no... what if last line has no '\n'?
        #    Better to strip out the '\n'. But strip() would make
        #    a copy of the string. Better yet, count occurences
        #    of '\n' per line and subtract them - this works in all
        #    cases, even for 0 '\n', and does not create unnecessary
        #    copies of the line-string.)
        #  - increment else_count for every 'else' word in the line
        for line in file_lines:
            char_count += len(line)
            newline_count += line.count('\n')
            else_count += line.count('else')

    return f'Lines: {len(file_lines)}, \
\'else\' statements: {else_count}, \
characters: {char_count} ({char_count - newline_count} excluding \'\\n\')'


def main():
    print(f'\n---------- {__file__} ----------')
    print(read_file())


if __name__ == '__main__':
    main()
