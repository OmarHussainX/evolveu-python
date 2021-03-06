import csv
# from collections import OrderedDict


def census_report(filename):
    """
    Receive parameter 'filename', which references a csv file containing
    community census data from the City of Calgary.
    Generates 'census_report.txt', containing information on the number
    of lines/records processed, and sums of RES_CNT (resident count) by
    CLASS (Industrial, Residential, etc.) and SECTOR (NW, SE, etc.).
    """
    with open(filename, mode='r') as csv_file:
        # Obtain a reader object which can be used to iterate over the rows of
        # the spreadsheet - the data in each row is mapped to a dictionary
        # (specifically, an OrderedDict dictionary)
        csv_reader = csv.DictReader(csv_file)

        # Initialise line/record count, and dictionaries for the total
        # resident counts by class, and by sector
        line_count = 0
        res_cnt_by_class = {}
        res_cnt_by_sector = {}

        # Iterate over the rows, and...
        for row in csv_reader:
            line_count += 1

            # ...build up dictionaries of the items we're interested in:
            # For each iteration/row, use the _value_ from the 'CLASS' or
            # 'SECTOR' column as a key in the respective dictionary:
            #   - if the key already exists in the dictionary, take the
            #     existing value for the key and add the 'RES_CNT' value for
            #     the current iteration/row to it
            #   - if the key doesn't exist, add it to the dictionary, with
            #     the 'RES_CNT' value for the current iteration/row as its
            #     value
            if row["CLASS"] in res_cnt_by_class:
                res_cnt_by_class[row["CLASS"]] += int(row["RES_CNT"])
            else:
                res_cnt_by_class[row["CLASS"]] = int(row["RES_CNT"])

            if row["SECTOR"] in res_cnt_by_sector:
                res_cnt_by_sector[row["SECTOR"]] += int(row["RES_CNT"])
            else:
                res_cnt_by_sector[row["SECTOR"]] = int(row["RES_CNT"])

        # Sort the dictionaries by key (for ouptut)
        #   - obtain a list[] of tuples(,) for each key:value pair
        #   - use sorted() to sort the list
        #   - construct a new OrderedDict from the sorted list (using
        #     OrderedDict is essential as a regular dictionary would not
        #     preserve insertion order when iterating over it)
        #
        # res_cnt_by_class = OrderedDict(sorted(res_cnt_by_class.items()))
        # res_cnt_by_sector = OrderedDict(sorted(res_cnt_by_sector.items()))
        #
        # Note: Taking alternative approach to the above - instead of creating
        # sorted dictionaries, sort by key when preparing the report

        # Generate report
        with open('census_report.txt', 'w') as report:

            report.write(f'({line_count} records)\n\n\n')

            report.write('RESIDENT COUNT BY CLASS\n')
            report.write('-' * 32 + '\n')
            for key, val in sorted(res_cnt_by_class.items()):
                report.write(format(key, '20') + format(val, '12,d') + '\n')

            report.write('\n\n')

            report.write('RESIDENT COUNT BY SECTOR\n')
            report.write('-' * 32 + '\n')
            for key, val in sorted(res_cnt_by_sector.items()):
                report.write(format(key, '20') + format(val, '12,d') + '\n')


def main():
    # print(f'\n---------- {__file__} ----------')
    census_report('Census_by_Community_2018.csv')


if __name__ == '__main__':
    main()
