import os
import pandas as pd
from re import match

from Perfume import Perfume
from PerfumeMap import PerfumeMap

from utility import make_sex_uniform
from utility import nan_to_none

from process_file_2 import *
from process_file_5 import *


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
    # Unnamed: 6 -> Price
    # Kind -> volume_set, volume_tester, volume_metadata
    # Description (fetch) -> volume_amount
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


def process_type_file_4(perfumeType):
    if pd.isna(perfumeType):
        return {"volume_set": False, "volume_tester": False, "volume_metadata": []}

    type_part_lists = perfumeType.split()
    volume_set = 'SET' in type_part_lists
    volume_tester = 'Tester' in type_part_lists

    volume_metadata = list(
        filter(lambda v: (v != 'SET' and v != 'Tester'), type_part_lists))

    return {"volume_set": volume_set, "volume_tester": volume_tester, "volume_metadata": volume_metadata}


def process_file_4(perfume_map, excel_file):
    data = pd.read_excel(excel_file, skiprows=[0, 1])

    # data = data.dropna(subset=["Brand", "Annie ", "Type", "Sex", "Size", "Unnamed: 6"])
    # print(len(data))
    # Unnamed: 6 -> Price

    perfume_list = [
        Perfume(perfume.Brand, perfume._3, None,
                make_sex_uniform(perfume.Sex),
                process_type_file_4(perfume.Type)["volume_tester"],
                process_type_file_4(perfume.Type)["volume_set"],
                nan_to_none(perfume.Size),
                process_type_file_4(perfume.Type)["volume_metadata"],
                perfume._7, 4)
        for perfume in data.itertuples()
    ]
    for p in perfume_list:
        perfume_map.insert_perfume(p)


def process_naziv_file_6(naziv):
    naziv_part_lists = naziv.split(" / ")

    return {"description": naziv_part_lists[0], "sex": make_sex_uniform(naziv_part_lists[2]),
            "volume_amount": naziv_part_lists[1]}


def process_tip_file_6(tip):
    volume_set = tip == 'Set'
    volume_tester = tip == 'Tester'

    return {"volume_set": volume_set, "volume_tester": volume_tester}


def process_file_6(perfume_map, excel_file):
    data = pd.read_excel(excel_file)

    # Naziv kreatora == _1 -> Brand
    # Naziv -> Description, volume_amount, sex

    perfume_list = [
        Perfume(perfume._1,
                process_naziv_file_6(perfume.Naziv)["description"],
                perfume.Tip,
                process_naziv_file_6(perfume.Naziv)["sex"],
                process_tip_file_6(perfume.Tip)["volume_tester"],
                process_tip_file_6(perfume.Tip)["volume_set"],
                process_naziv_file_6(perfume.Naziv)["volume_amount"],
                [],
                perfume.Cena, 6)
        for perfume in data.itertuples()
    ]
    for p in perfume_list:
        print(p)
        perfume_map.insert_perfume(p)


def make_ml_lowercase(volume):
    if pd.isna(volume):
        return None
    return volume[0:-2] + volume[-2:].lower()


def process_group_file_7(group):
    volume_set = group == 'set'
    volume_tester = group == 'TESTER'

    volume_metadata = []
    if volume_set == False and volume_tester == False:
        volume_metadata = [group]

    return {"volume_set": volume_set, "volume_tester": volume_tester, "volume_metadata": volume_metadata}


def process_file_7(perfume_map, excel_file):
    data = pd.read_excel(excel_file)

    data = data.dropna(subset=["PIRCE"])
    # BRANDS -> Brand
    # Naziv -> Description, volume_amount, sex

    perfume_list = [
        Perfume(perfume.BRANDS, perfume._3, perfume.TYPE,
                "U",
                process_group_file_7(perfume.GROUP)["volume_tester"],
                process_group_file_7(perfume.GROUP)["volume_set"],
                make_ml_lowercase(perfume.SIZE),
                process_group_file_7(perfume.GROUP)["volume_metadata"],
                perfume.PIRCE, 7)
        for perfume in data.itertuples()
    ]
    for p in perfume_list:
        perfume_map.insert_perfume(p)
        # print(p)


def main():
    root_folder = "data"
    perfume_map1 = PerfumeMap()
    perfume_map2 = PerfumeMap()
    perfume_map = PerfumeMap()
    for root, dirs, files in os.walk(root_folder):
        for filename in files:

            if filename == "2.xlsx":
                process_file_2(perfume_map, os.path.join(root, filename))
#            elif filename == "3.xlsx":
#                process_file_3(perfume_map, os.path.join(root, filename))
#            elif filename == "4.xlsx":
#                process_file_4(perfume_map, os.path.join(root, filename))
            if filename == "5.xlsx":
                process_file_5(perfume_map, os.path.join(root, filename))
#            elif filename == "6.xls":
#                process_file_6(perfume_map, os.path.join(root, filename))
#            elif filename == "7.xlsx":
#                process_file_7(perfume_map, os.path.join(root, filename))


    #print(perfume_map)

    for p in perfume_map.get_map()[('CHRISTIAN DIOR', 'DIOR HOMME INTENSE')]:
        print(p)

#    print(perfume_map1)
    #print()
    #for p in perfume_map1.get_map()[('CHRISTIAN DIOR', 'DIOR HOMME INTENSE')]:
    #    print(p)


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
