import os

from process_file_2 import *
from process_file_3 import *
from process_file_4 import *
from process_file_5 import *
from process_file_6 import *
from process_file_7 import *
from process_file_D1 import *
from process_file_Lager import *
from process_file_DV import *


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
        output_perfume_list_with_prices['Price'].append(perfume_map.get_minimal_price_and_parent_file(key)[0])
        output_perfume_list_with_prices['File'].append(map_file_number_to_filename(perfume_map.get_minimal_price_and_parent_file(key)[1]))

        output_perfume_list_without_prices['Brand'].append(key[0])
        output_perfume_list_without_prices['Description'].append(key[1])
        output_perfume_list_without_prices['Volume'].append(key[2])
        output_perfume_list_without_prices['Sex'].append(key[3])
        output_perfume_list_without_prices['Price'].append('')

    df = pd.DataFrame(output_perfume_list_with_prices)
    df = df.sort_values(['Brand'], ascending=[True])

    writer = pd.ExcelWriter(output_data_folder + xlsx_with_prices, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()

    df = pd.DataFrame(output_perfume_list_without_prices)
    df = df.sort_values(['Brand'], ascending=[True])
    writer = pd.ExcelWriter(output_data_folder + xlsx_without_prices, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()


def main():
    root_folder = "data"
    perfume_map = PerfumeMap()
    for root, dirs, files in os.walk(root_folder):
        for filename in files:

            if filename == "ALL.xlsx":
                process_file_2(perfume_map, os.path.join(root, filename))
            elif filename == "KULD.xlsx":
                process_file_4(perfume_map, os.path.join(root, filename))
            elif filename == "DDP.xlsx":
                process_file_7(perfume_map, os.path.join(root, filename))
            elif filename == "LILI.xlsx":
                process_file_5(perfume_map, os.path.join(root, filename))
            elif filename == "V2.xls":
                process_file_6(perfume_map, os.path.join(root, filename))
            elif filename == "LUCAS.xlsx":
                process_file_3(perfume_map, os.path.join(root, filename))
            elif filename == "D1.xls":
                process_file_D1(perfume_map, os.path.join(root, filename))
            elif filename == "Lager.xlsx":
                process_file_Lager(perfume_map, os.path.join(root, filename))
            elif filename == "DV.xls":
                process_file_DV(perfume_map, os.path.join(root, filename))

    write_combined_perfumes_to_xlsx(perfume_map)


if __name__ == "__main__":
    main()
