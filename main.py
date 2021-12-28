import os
import pandas as pd
from re import match

from Perfume import Perfume
import PerfumeMap


def process_volume_file_2(volume):
    print(volume)
    volume_part_lists = volume.split()
    volume_set = 'SET' in volume_part_lists
    volume_tester = 'Tester' in volume_part_lists

    volume_amount = list(filter(lambda v: match('^\d+ml$', v), volume_part_lists))
    if len(volume_amount) == 1:
        volume_amount = volume_amount[0]
    else:
        volume_amount = None

    volume_metadata = list(
        filter(lambda v: (not match('^\d+ml$', v) and v != 'SET' and v != 'Tester'), volume_part_lists))

    print(volume_set, volume_tester, "am:", volume_amount, "md: ", volume_metadata, volume_part_lists)


def process_file_2(perfume_map, excel_file):
    data = pd.read_excel(excel_file)
    data = data.dropna(subset=["Brand", "Description", "Type", "Sex", "Volume", "Net EUR"])
    print(data)
    #    perfume_list = [
    #        Perfume(perfume.Brand, perfume.Description, perfume.Type, perfume.Sex,
    #                volume_type, volume_set, volume_amount, perfume._7, 2) for perfume in data.itertuples()]

    i = 2
    for p in data.itertuples():
        print("\n")
        print(i)
        print(process_volume_file_2(p.Volume))
        i = i + 1


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
