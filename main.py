import os
import pandas as pd
from re import match

from Perfume import Perfume
from PerfumeMap import PerfumeMap


def make_sex_uniform(sex):
    if pd.isna(sex):
        return None
    sex = sex.upper()
    if sex == "MEN":
        return "M"
    elif sex == "MAN":
        return "M"
    elif sex == "MUŠKI":
        return "M"
    elif sex == "WOMEN":
        return "W"
    elif sex == "WOMAN":
        return "W"
    elif sex == "ŽENSKI":
        return "W"
    if sex == "UNISEX":
        return "U"
    else:
        return "U"


def nan_to_None(variable):
    if pd.isna(variable):
        return None
    return variable


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
                nan_to_None(perfume.Size),
                process_type_file_4(perfume.Type)["volume_metadata"],
                perfume._7, 4)
        for perfume in data.itertuples()
    ]
    for p in perfume_list:
        perfume_map.insert_perfume(p)


def process_unnamed_4_file_5(type):
    if type == "SET":
        return {"volume_set": True}
    else:
        return {"volume_set": False}


def process_unnamed_3_file_5(volume):
    volume_part_lists = volume.split()
    volume_tester = 'Tester' in volume_part_lists
    volume_amount = None

    if 'ml' in volume_part_lists:
        volume_amount = volume_part_lists[volume_part_lists.index('ml') - 1]

    volume_metadata = list(
        filter(lambda v: (v != volume_amount and v != 'ml' and v != 'Tester'), volume_part_lists))

    return {"volume_tester": volume_tester,
            "volume_amount": str(volume_amount) + "ml", "volume_metadata": volume_metadata}


def process_file_5(perfume_map, excel_file):
    data = pd.read_excel(excel_file)

    data = data.dropna(subset=["Unnamed: 5"])
    # Unnamed: 1 -> Brand
    # Unnamed: 2 -> Description
    # Unnamed: 4 -> Type
    # Unnamed: 4 (fetch) -> volume_set
    # Unnamed: 3 -> volume_amount, volume_tester, volume_metadata
    # Unnamed: 5 -> Price

    perfume_list = [
        Perfume(perfume._2, perfume._3, perfume._5,
                'U',
                process_unnamed_3_file_5(perfume._4)["volume_tester"],
                process_unnamed_4_file_5(perfume._3)["volume_set"],
                process_unnamed_3_file_5(perfume._4)["volume_amount"],
                process_unnamed_3_file_5(perfume._4)["volume_metadata"],
                perfume._6, 5)
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
        perfume_map.insert_perfume(p)


def process_file_7(perfume_map, excel_file):
    data = pd.read_excel(excel_file)

    # BRANDS -> Brand
    # Naziv -> Description, volume_amount, sex

    perfume_list = [
        (perfume.BRANDS,
        perfume._3)
        for perfume in data.itertuples()
    ]
    for p in perfume_list:
        #perfume_map.insert_perfume(p)
        print(p)


def main():
    root_folder = "data"
    perfume_map1 = PerfumeMap()
    perfume_map2 = PerfumeMap()
    perfume_map = PerfumeMap()
    for root, dirs, files in os.walk(root_folder):
        for filename in files:
            """
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
            if filename == "7.xlsx":
                process_file_7(perfume_map, os.path.join(root, filename))
    print(len(perfume_map.get_map()))
    print(perfume_map)
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
