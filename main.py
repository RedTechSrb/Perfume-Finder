import os
import pandas as pd
from re import match

from Perfume import Perfume
from PerfumeMap import PerfumeMap

from utility import make_sex_uniform
from utility import nan_to_none

from process_file_2 import *
from process_file_3 import *
from process_file_4 import *
from process_file_5 import *





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
            elif filename == "3.xlsx":
                process_file_3(perfume_map, os.path.join(root, filename))
            elif filename == "4.xlsx":
                process_file_4(perfume_map, os.path.join(root, filename))
            elif filename == "5.xlsx":
                process_file_5(perfume_map, os.path.join(root, filename))
#            elif filename == "6.xls":
#                process_file_6(perfume_map, os.path.join(root, filename))
#            elif filename == "7.xlsx":
#                process_file_7(perfume_map, os.path.join(root, filename))



    for p in perfume_map.get_map()[('CHRISTIAN DIOR',
                                    'DIOR HOMME')]:
        print(p)
    print()

    for p in perfume_map.get_map()[('CHRISTIAN DIOR',
                                    'DIOR HOMME INTENSE')]:
        print(p)
    print()

    for p in perfume_map.get_map()[('CHRISTIAN DIOR',
                                     'DIOR HOMME EDT')]:
        print(p)
    print()
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
