from Perfume import Perfume
from PerfumeMap import PerfumeMap

from utility import *


def process_unnamed_4_file_5(column_4_data):
    if pd.isna(column_4_data):
        return {"volume_tester": None, "volume_amount": None, "volume_metadata": None}

    volume_part_lists = column_4_data.split()
    volume_tester = 'Tester' in volume_part_lists

    if 'ml' in volume_part_lists:
        volume_amount = volume_part_lists[volume_part_lists.index('ml') - 1]

        volume_metadata = list(
            filter(lambda v: (v != volume_amount and v != 'ml' and v != 'Tester'), volume_part_lists))

        return {"volume_tester": volume_tester,
                "volume_amount": str(volume_amount) + "ml",
                "volume_metadata": volume_metadata}

    else:

        volume_metadata = list(
            filter(lambda v: (v != 'ml' and v != 'Tester'), volume_part_lists))

        return {"volume_tester": volume_tester,
                "volume_amount": None,
                "volume_metadata": volume_metadata}


def process_unnamed_3_file_5(column_3_data):
    if pd.isna(column_3_data):
        return {"sex": None}
    column_3_data = column_3_data.upper()
    if column_3_data.find('WOMEN & MEN') != -1:
        return {"sex": "U"}
    elif column_3_data.find('UNISEX') != -1:
        return {"sex": "U"}
    elif column_3_data.find('WOMAN') != -1:
        return {"sex": "W"}
    elif column_3_data.find('WOMEN') != -1:
        return {"sex": "W"}
    elif column_3_data.find('MAN') != -1:
        return {"sex": "M"}
    elif column_3_data.find('MEN') != -1:
        return {"sex": "M"}

    return {"sex": "N"}


def process_unnamed_5_file_5(column_5_data):
    if pd.isna(column_5_data):
        return {"volume_set": None, "Type": None}

    perfume_type = column_5_data
    volume_set = 'Set' == column_5_data

    if volume_set:
        perfume_type = None

    return {"volume_set": volume_set, "Type": perfume_type}


def process_file_5(perfume_map: PerfumeMap, excel_file):

    print("File 5.xlsx processing ... ")

    data = pd.read_excel(excel_file)

    # file_5 specificity
    # _2 -> Brand
    # _3 -> Description, sex
    # _4 -> volume_tester, volume_amount, volume_metadata
    # _5 -> Type, volume_set
    # _6 -> Price

    perfume_list = [
        Perfume(str(perfume._2),
                str(perfume._3),
                str(process_unnamed_5_file_5(perfume._5)["Type"]),
                process_unnamed_3_file_5(perfume._3)["sex"],
                process_unnamed_4_file_5(perfume._4)["volume_tester"],
                process_unnamed_5_file_5(perfume._5)["volume_set"],
                process_unnamed_4_file_5(perfume._4)["volume_amount"],
                process_unnamed_4_file_5(perfume._4)["volume_metadata"],
                perfume._6,
                5)
        for perfume in data.itertuples()
    ]

    for p in perfume_list:
        perfume_map.insert_perfume(p)

    print("... finished")
