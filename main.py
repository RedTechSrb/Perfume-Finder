import os
import pandas as pd
from re import match

from Perfume import Perfume
from PerfumeMap import PerfumeMap


def make_sex_uniform(sex):

    if sex == "MEN":
        return "M"
    elif sex == "MAN":
        return "M"
    elif sex == "WOMEN":
        return "W"
    elif sex == "WOMAN":
        return "W"
    if sex == "UNISEX":
        return "U"
    else:
        return "U"


def process_volume_file_2(volume):

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

    return {"volume_set": volume_set, "volume_tester": volume_tester,
            "volume_amount": volume_amount, "volume_metadata": volume_metadata}


def process_file_2(perfume_map: PerfumeMap, excel_file):
    data = pd.read_excel(excel_file)
    data = data.dropna(subset=["Brand", "Description", "Type", "Sex", "Volume", "Net EUR"])
    # Volume -> volume_set, volume_tester, volume_amount, volume_metadata
    perfume_list = [
        Perfume(perfume.Brand, perfume.Description, perfume.Type,
                make_sex_uniform(perfume.Sex),
                process_volume_file_2(perfume.Volume)["volume_tester"],
                process_volume_file_2(perfume.Volume)["volume_set"],
                process_volume_file_2(perfume.Volume)["volume_amount"],
                process_volume_file_2(perfume.Volume)["volume_metadata"],
                perfume._7, 2)
        for perfume in data.itertuples()
    ]
    for p in perfume_list:
        perfume_map.insert_perfume(p)


def process_kind_file_3(kind):

    kind_part_lists = kind.split()
    volume_set = 'SET' in kind_part_lists
    volume_tester = 'TESTER' in kind_part_lists

    volume_metadata = list(
        filter(lambda v: (v != 'SET' and v != 'Tester'), kind_part_lists))

    return {"volume_set": volume_set, "volume_tester": volume_tester, "volume_metadata": volume_metadata}


def process_description_file_3(description):

    description_part_lists = description.split()

    volume_amount = list(filter(lambda v: match('^\d+ml$', v), description_part_lists))

    if len(volume_amount) == 1:
        volume_amount = volume_amount[0]
    else:
        volume_amount = None  # Check this

    return {"volume_amount": volume_amount}


def process_file_3(perfume_map, excel_file):
    data = pd.read_excel(excel_file, skiprows=[0])
    data = data.dropna(subset=["Kind", "Sex", "Unnamed: 3", "Description", "Unnamed: 5"])
    # Unnamed: 3 -> Brand

    perfume_list = [
        Perfume(perfume._4, perfume.Description, None,
                perfume.Sex,
                process_kind_file_3(perfume.Kind)["volume_tester"],
                process_kind_file_3(perfume.Kind)["volume_set"],
                process_description_file_3(perfume.Description)["volume_amount"],
                process_kind_file_3(perfume.Kind)["volume_metadata"],
                perfume._6, 3)
        for perfume in data.itertuples()
    ]
    for p in perfume_list:
        perfume_map.insert_perfume(p)


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
    perfume_map1 = PerfumeMap()
    perfume_map2 = PerfumeMap()
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

    print(len(perfume_map.get_map()))
    """
    PROBLEM None ne poredi sa EDDT kao true nego kao false
    print(len(perfume_map1.get_map()))
    print(len(perfume_map2.get_map()))
    print(perfume_map1)

    pp1 = Perfume('ZEGNA', 'ZEGNA FORTE', None,
                 'M',
                 False,
                 False,
                 '100ml',
                 [],
                 88.22, 9)
    perfume_map1.insert_perfume(pp1)

    print(perfume_map1)
    """

if __name__ == "__main__":
    main()
