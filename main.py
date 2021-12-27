import os
import pandas as pd

import PerfumeMap


def process_volume_file_2(volume):
    print(volume)
    print(volume.split())


def process_file_2(perfume_map, excel_file):

    data = pd.read_excel(excel_file)
    # perfume_list = data[["Brand", "Description", "Type", "Sex", "Volume", "Net EUR"]]
    #print(type(perfume_list))
    #A = [Silly(a.one, a.two) for a in df.itertuples()]
    x = set()
    for a in data.itertuples():
        #print(a.Brand, a.Description, a.Type, a.Sex, a.Volume, a._7)
        x.add(a.Volume)
        process_volume_file_2(a.Volume)
    print(x)


def process_file_3(perfume_map, excel_file):
    pass


def process_file_4(perfume_map, excel_file):
    pass


def process_file_5(perfume_map, excel_file):
    pass


def process_file_6(perfume_map, excel_file):
    pass


def process_file_7(perfume_map, excel_file):
    pass


def main():
    root_folder = "data"
    perfume_map = PerfumeMap

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
            elif filename == "6.xlsx":
                process_file_6(perfume_map, os.path.join(root, filename))
            elif filename == "7.xlsx":
                process_file_7(perfume_map, os.path.join(root, filename))


if __name__ == "__main__":
    main()
