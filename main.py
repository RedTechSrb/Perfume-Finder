import os

import pandas as pd

from process_file_2 import *
from process_file_3 import *
from process_file_4 import *
from process_file_5 import *
from process_file_6 import *
from process_file_7 import *


def write_combined_perfumes_to_xlsx(perfume_map: PerfumeMap):
    output_data_folder = "output_data/"
    xlsx_with_prices = "perfumes_with_prices.xlsx"
    xlsx_without_prices = "perfumes_without_prices.xlsx"

    output_perfume_list_with_prices = {'Brand': [],
                                       'Description': [],
                                       'Volume': [],
                                       'Sex': [],
                                       'File': [],
                                       'Price': []
                                       }

    output_perfume_list_without_prices = {'Brand': [],
                                          'Description': [],
                                          'Volume': [],
                                          'Sex': [],
                                          'Price': []
                                          }

    for key, value in perfume_map.get_map().items():
        #print(key[0], key[1], key[2], key[3], perfume_map.get_minimal_price_and_parent_file(key)[0], perfume_map.get_minimal_price_and_parent_file(key)[1])

        output_perfume_list_with_prices['Brand'].append(key[0])
        output_perfume_list_with_prices['Description'].append(key[1])
        output_perfume_list_with_prices['Volume'].append(key[2])
        output_perfume_list_with_prices['Sex'].append(key[3])
        output_perfume_list_with_prices['File'].append(perfume_map.get_minimal_price_and_parent_file(key)[0])
        output_perfume_list_with_prices['Price'].append(perfume_map.get_minimal_price_and_parent_file(key)[1])

        output_perfume_list_without_prices['Brand'].append(key[0])
        output_perfume_list_without_prices['Description'].append(key[1])
        output_perfume_list_without_prices['Volume'].append(key[2])
        output_perfume_list_without_prices['Sex'].append(key[3])
        output_perfume_list_without_prices['Price'].append('')

    df = pd.DataFrame(output_perfume_list_with_prices)
    writer = pd.ExcelWriter(output_data_folder + xlsx_with_prices, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()

    df = pd.DataFrame(output_perfume_list_without_prices)
    writer = pd.ExcelWriter(output_data_folder + xlsx_without_prices, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()


def main():
    root_folder = "data"
    perfume_map = PerfumeMap()
    for root, dirs, files in os.walk(root_folder):
        for filename in files:

            if filename == "2.xlsx":
                process_file_2(perfume_map, os.path.join(root, filename))
            elif filename == "3.xlsx":
                process_file_3(perfume_map, os.path.join(root, filename))
            elif filename == "4.xlsx":
                process_file_4(perfume_map, os.path.join(root, filename))
            elif filename == "5.xlsx":
                process_file_5(perfume_map, os.path.join(root, filename))
            elif filename == "6.xls":
                process_file_6(perfume_map, os.path.join(root, filename))
            elif filename == "7.xlsx":
                process_file_7(perfume_map, os.path.join(root, filename))

    """
    for p in perfume_map.get_map()[('CD',
                                    'DIOR HOMME',
                                    '100ml',
                                    'M')]:
        print(p)
    print()

    for p in perfume_map.get_map()[('CHRISTIAN DIOR',
                                    'DIOR HOMME',
                                    None,
                                    'M')]:
        print(p)
    print()

    for p in perfume_map.get_map()[('CHRISTIAN DIOR',
                                    'DIOR HOMME',
                                    '100ml',
                                    'M')]:
        print(p)
    print()

    for p in perfume_map.get_map()[('CHRISTIAN DIOR',
                                    'DIOR HOMME',
                                    '75ml',
                                    'M')]:
        print(p)
    print()

    for p in perfume_map.get_map()[('CHRISTIAN DIOR',
                                    'DIOR HOMME INTENSE',
                                    '100ml',
                                    'M')]:
        print(p)
    print()

    for p in perfume_map.get_map()[('CHRISTIAN DIOR',
                                    'DIOR HOMME EDT',
                                    '100ml',
                                    'M')]:
        print(p)
    print()
    
    print(perfume_map.get_minimal_price_and_parent_file(('CHRISTIAN DIOR', 'DIOR HOMME', '100ml', 'M')))
    print(perfume_map.get_minimal_price_and_parent_file(('CHRISTIAN DIOR', 'DIOR HOMME INTENSE', '100ml', 'M')))
    print(perfume_map.get_minimal_price_and_parent_file(('CHRISTIAN DIOR', 'DIOR HOMME EDT', '100ml', 'M')))
    print(perfume_map.get_minimal_price_and_parent_file(('CD', 'DIOR HOMME', '100ml', 'M')))
    """
    write_combined_perfumes_to_xlsx(perfume_map)


if __name__ == "__main__":
    main()
