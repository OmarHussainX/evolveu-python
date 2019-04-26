import os

def folder_report():
    """
    Generates a 'folder_info.txt' report for a specified folder, with
    information on the entries (files, folders - excluding '.', '..')
    therein, the total number of entires, and their size
    """
    path = '/home/omar/Downloads'
    file_list = []
    folder_list = []
    col_width = 12   #

    # Obtain an iterator of os.DirEntry objects for the specified
    # path, and use that to iterate through the entries (files & folders)
    # in the folder
    # For each entry generate a tuple: (name, size)
    #
    # Note:
    #   The iterator excludes '.' '..'
    #   The items are in _arbitrary_ order
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
        """
        Helper function,
        Used to sort files & folders alphabetically
        """
        return val[0].lower()

    def format_size(val):
        """
        Helper function,
        Receives file-size in bytes as a _number_, converts the size to
        a kb, Mb, Gb, _string_, and right-justifies the string
        """
        if val < 1024:
            val = f'{val} b '
        elif val < 1048576:
            val = f'{round(val/1024, 1)} kb'
        elif val < 1073741824:
            val = f'{round(val/1048576, 1)} Mb'
        elif val < 1099511627776:
            val = f'{round(val/1073741824, 1) } Gb'

        return f'{" " * (col_width - len(val))}{val}'


    # sort the file & folder lists
    folder_list.sort(key=case_insensitive)
    file_list.sort(key=case_insensitive)

    # calculate the total file size
    total_file_size = 0
    for file in file_list:
        total_file_size += file[1]
    
    total_file_size = format_size(total_file_size).strip()



    # generate the report
    print(f'{path}\n\n\
{len(folder_list)} folders\n\
{len(file_list)} files (total: {total_file_size})\n')

    for folder in folder_list:
        print(f' {format_size(folder[1])}  {folder[0]}')


    for file in file_list:
        print(f' {format_size(file[1])}  {file[0]}')


def main():
    # print(f'---------- {__file__} ----------\n')
    folder_report()


if __name__ == '__main__':
    main()
