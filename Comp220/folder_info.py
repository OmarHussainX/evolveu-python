import os

def folder_report():
    """
    Generates a 'folder_info.txt' report for a specified folder with
    information on the entries (files, folders - excluding '.', '..')
    therein, the total number of entires, and their size
    """
    path = '/home/omar/Downloads'
    file_list = []
    folder_list = []
    colwidth = 12

    # Obtain an iterator of os.DirEntry objects for the specified
    #  path (excluding '.' '..')
    #
    # Note:
    #   The items are in arbitrary order
    #   scandir() preferable to listdir() when requesting file type/attribute data,
    #   because DirEntry objects expose this info. when scanning directories on
    #   supported operating systems
    with os.scandir(path) as dir_entry_iterator:
        for entry in dir_entry_iterator:
            if entry.is_file():
                file_list.append((entry.name, entry.stat().st_size))
            else:
                folder_list.append((entry.name, entry.stat().st_size))

    def case_insensitive(val):
        return val[0].lower()


    def format_size(val):
        if val < 1024:
            val = f'{val} b '
        elif val < 1048576:
            val = f'{round(val/1024, 1)} kb'
        elif val < 1073741824:
            val = f'{round(val/1048576, 1)} Mb'
        elif val < 1099511627776:
            val = f'{round(val/1073741824, 1) } Gb'

        return f'{" " * (colwidth-len(val))}{val}'


    folder_list.sort(key=case_insensitive)

    for folder in folder_list:
        print(f' {format_size(folder[1])}  {folder[0]}')


    file_list.sort(key=case_insensitive)
    for file in file_list:
        print(f' {format_size(file[1])}  {file[0]}')


def main():
    print(f'\n---------- {__file__} ----------')
    folder_report()


if __name__ == '__main__':
    main()
