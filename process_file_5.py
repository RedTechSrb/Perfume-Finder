from re import match

from Perfume import Perfume
from PerfumeMap import PerfumeMap

from utility import *


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


def process_unnamed_5_file_5(column_5_data):
    if pd.isna(column_5_data):
        return {"volume_set": None, "Type": None}

    perfume_type = column_5_data
    volume_set = 'Set' == column_5_data

    if volume_set:
        perfume_type = None

    return {"volume_set": volume_set, "Type": perfume_type}


def process_file_5(perfume_map: PerfumeMap, excel_file):
    data = pd.read_excel(excel_file)

    # file_5 specificity
    # _2 -> Brand
    # _3 -> Description
    # _4 -> volume_tester, volume_amount, volume_metadata
    # _5 -> Type, volume_set
    # _6 -> Price

    for perfume in data.itertuples():
        print(perfume._2, "#",
              perfume._3, "#",
              process_unnamed_5_file_5(perfume._5)["Type"], "#",
#                'U', "#",
#                process_unnamed_3_file_5(perfume._4)["volume_tester"], "#",
                process_unnamed_5_file_5(perfume._3)["volume_set"], "#",
#                process_unnamed_3_file_5(perfume._4)["volume_amount"], "#",
 #               process_unnamed_3_file_5(perfume._4)["volume_metadata"], "#",
 #               perfume._6,  "#",

              5)

#    perfume_list = [
#        Perfume(perfume._2, perfume._3, perfume._5,
#                'U',
#                process_unnamed_3_file_5(perfume._4)["volume_tester"],
#                process_unnamed_4_file_5(perfume._3)["volume_set"],
#                process_unnamed_3_file_5(perfume._4)["volume_amount"],
#                process_unnamed_3_file_5(perfume._4)["volume_metadata"],
#                perfume._6, 5)
#        for perfume in data.itertuples()
#    ]
#    for p in perfume_list:
#        perfume_map.insert_perfume(p)