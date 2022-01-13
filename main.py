import os
import pandas as pd
from re import match

from Perfume import Perfume
from PerfumeMap import PerfumeMap


def process_volume_file_2(volume):
    #print(volume)
    volume_part_lists = volume.split()
    volume_set = 'SET' in volume_part_lists
    volume_tester = 'Tester' in volume_part_lists

    volume_amount = list(filter(lambda v: match('^\d+ml$', v), volume_part_lists))
    if len(volume_amount) == 1:
        volume_amount = volume_amount[0]
    else:
        volume_amount = None  # Check this

    volume_metadata = list(
        filter(lambda v: (not match('^\d+ml$', v) and v != 'SET' and v != 'Tester'), volume_part_lists))

    #print("set:", volume_set, "tst:", volume_tester, "am:", volume_amount, "md: ", volume_metadata, volume_part_lists)
    return {"volume_set": volume_set, "volume_tester": volume_tester,
            "volume_amount": volume_amount, "volume_metadata": volume_metadata}


def process_file_2(perfume_map: PerfumeMap, excel_file):
    data = pd.read_excel(excel_file)
    data = data.dropna(subset=["Brand", "Description", "Type", "Sex", "Volume", "Net EUR"])
    # Volume -> volume_set, volume_tester, volume_amount, volume_metadata

    perfume_list = [
        Perfume(perfume.Brand, perfume.Description, perfume.Type, perfume.Sex,
                process_volume_file_2(perfume.Volume)["volume_tester"],
                process_volume_file_2(perfume.Volume)["volume_set"],
                process_volume_file_2(perfume.Volume)["volume_amount"],
                process_volume_file_2(perfume.Volume)["volume_metadata"],
                perfume._7, 2)
        for perfume in data.itertuples()
    ]
    for p in perfume_list:
        perfume_map.insert_perfume(p)


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
            elif filename == "6.xlsx":
                process_file_6(perfume_map, os.path.join(root, filename))
            elif filename == "7.xlsx":
                process_file_7(perfume_map, os.path.join(root, filename))

    print(perfume_map)


if __name__ == "__main__":
    main()
