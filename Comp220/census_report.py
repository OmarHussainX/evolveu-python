import csv

def census_report(filename):
    """
    Receive parameter 'filename', which references a csv file containing
    community census data from the City of Calgary.
    Generates a 'census_report.txt' report, with information on the
    number of lines/records processed, and sums of RES_CNT (resident count)
    by CLASS (Industrial, Residential, etc.) and SECTOR (NW, SE, etc.).
    """
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        res_cnt_by_class = {}
        res_cnt_by_sector = {}

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                
            
            # print(f'\tCLASS: {row["CLASS"]}, RES_CNT: {row["RES_CNT"]}')
            line_count += 1
            
            # build up dictionary of items were interested in...
            # for each iteration/row, use the _value_from the 'CLASS' column
            # as a kaey in a dictionary:
            #   - if the key exists, take the exisiting value and add the
            #     'RES_CNT' value for he row tro it
            #   - if the key doesn't exist, add it to the dictionary, with
            #     'RES_CNT' as value
            #
            if row["CLASS"] in res_cnt_by_class:
                res_cnt_by_class[row["CLASS"]] += int(row["RES_CNT"])
            else:
                res_cnt_by_class[row["CLASS"]] = int(row["RES_CNT"])

            if row["SECTOR"] in res_cnt_by_sector:
                res_cnt_by_sector[row["SECTOR"]] += int(row["RES_CNT"])
            else:
                res_cnt_by_sector[row["SECTOR"]] = int(row["RES_CNT"])


        print(f'({line_count} records)\n')
        print(f'RES_CNT by CLASS {res_cnt_by_class}\n')
        print(f'RES_CNT by SECTOR {res_cnt_by_sector}')


def main():
    print(f'\n---------- {__file__} ----------')
    census_report('Census_by_Community_2018.csv')


if __name__ == '__main__':
    main()
