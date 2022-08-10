import re
from re import match

from Perfume import Perfume
from PerfumeMap import PerfumeMap

from utility import *


def process_unnamed_1_file_8(column_1_data):

    volume_type_search = 'edp' in column_1_data
    volume_type = 'NAN'
    if volume_type_search:
        volume_type = 'edp'
        column_1_data = column_1_data.replace('edp', '')

    volume_type_search = 'edt' in column_1_data
    if volume_type_search:
        volume_type = 'edt'
        column_1_data = column_1_data.replace('edt', '')

    volume_amount_search = re.search('^(.*)  *(\d*ml)(.*)$', column_1_data, re.IGNORECASE)

    if volume_amount_search:
        Description = volume_amount_search.group(1) + " " + volume_amount_search.group(3)
        volume_amount = volume_amount_search.group(2)
        volume_metadata = []
    else:
        Description = 'NAN'
        volume_amount = 'NAN'
        volume_metadata = 'NAN'

    return {"Description": Description,
            "Type": volume_type,
            "volume_amount": volume_amount,
            "volume_metadata": volume_metadata}


def process_unnamed_2_file_8(column_2_data):

    brand_sex_set_tester_search = re.search('^(.*)( *)\(([a-zA-Z]*)(.*) \\\\ (.*)\)$', column_2_data, re.IGNORECASE)

    if brand_sex_set_tester_search:
        brand = brand_sex_set_tester_search.group(1)
        sex = brand_sex_set_tester_search.group(3)
        set_tester = brand_sex_set_tester_search.group(5)

        return {"Brand": brand,
                "sex": sex,
                "volume_set": 'SETOVI' in set_tester,
                "volume_tester": 'TESTERI' in set_tester}

    return {"Brand": 'NAN',
            "sex": 'NAN',
            "volume_set": 'NAN',
            "volume_tester": 'NAN'}


def process_file_D1(perfume_map: PerfumeMap, excel_file):

    print("File D1.xls processing ... ")

    data = pd.read_excel(excel_file, header=None)

    # _1 -> Description, Type, volume_amount, volume_metadata
    # _2 -> Brand, sex, volume_set, volume_tester
    # _3 -> Price

    perfume_list = [
        Perfume(
                process_unnamed_2_file_8(perfume._2)["Brand"],
                process_unnamed_1_file_8(perfume._1)["Description"],
                process_unnamed_1_file_8(perfume._1)["Type"],
                make_sex_uniform(process_unnamed_2_file_8(perfume._2)["sex"]),
                process_unnamed_2_file_8(perfume._2)["volume_tester"],
                process_unnamed_2_file_8(perfume._2)["volume_set"],
                process_unnamed_1_file_8(perfume._1)["volume_amount"],
                process_unnamed_1_file_8(perfume._1)["volume_metadata"],
                perfume._3,
                8)
        for perfume in data.itertuples()
    ]
    for p in perfume_list:
        perfume_map.insert_perfume(p)

    print("... finished")
