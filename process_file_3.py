from re import match

from Perfume import Perfume
from PerfumeMap import PerfumeMap

from utility import *


def process_kind_file_3(kind_data):
    if pd.isna(kind_data):
        return {"volume_set": None, "volume_tester": None, "volume_metadata": None}

    kind_part_lists = kind_data.split()
    volume_set = 'SET' in kind_part_lists
    volume_tester = 'TESTER' in kind_part_lists

    volume_metadata = list(filter(lambda v: (v != 'SET' and v != 'TESTER'), kind_part_lists))

    return {"volume_set": volume_set, "volume_tester": volume_tester, "volume_metadata": volume_metadata}


def process_description_file_3(description_data):
    if pd.isna(description_data):
        return {"volume_amount": None, "Description": None}

    description_part_lists = description_data.split()

    volume_amount = list(filter(lambda v: match('^\d+ml$', v), description_part_lists))

    if len(volume_amount) == 1:
        volume_amount = volume_amount[0]
        description = ' '.join(list(filter(lambda v: (v != volume_amount), description_part_lists)))
    else:
        volume_amount = None  # Check this
        description = description_data

    return {"volume_amount": volume_amount, "Description": description}


def process_file_3(perfume_map: PerfumeMap, excel_file):
    data = pd.read_excel(excel_file, skiprows=[0])

    # file_3 specificity
    # Kind -> volume_tester, volume_set, volume_metadata
    # _4 -> Brand
    # Description -> Description, volume_amount
    # _6 -> Price

    # for perfume in data.itertuples():
    #
    #     print(perfume._4, " #",
    #           process_description_file_3(perfume.Description)["Description"], "# ",
    #           None, " # ",
    #         make_sex_uniform(perfume.Sex), " # ",
    #             process_kind_file_3(perfume.Kind)["volume_tester"], " # ",
    #             process_kind_file_3(perfume.Kind)["volume_set"], " # ",
    #           process_description_file_3(perfume.Description)["volume_amount"], " # ",
    #           process_kind_file_3(perfume.Kind)["volume_metadata"], " # ",
    #             perfume._6, " # ",
    #           3)

    perfume_list = [
        Perfume(str(perfume._4),
                str(process_description_file_3(perfume.Description)["Description"]),
                str(None),
                make_sex_uniform(perfume.Sex),
                process_kind_file_3(perfume.Kind)["volume_tester"],
                process_kind_file_3(perfume.Kind)["volume_set"],
                process_description_file_3(perfume.Description)["volume_amount"],
                process_kind_file_3(perfume.Kind)["volume_metadata"],
                perfume._6,
                3)
        for perfume in data.itertuples()
    ]
    for p in perfume_list:
        perfume_map.insert_perfume(p)
