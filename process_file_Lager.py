from Perfume import Perfume
from PerfumeMap import PerfumeMap

from utility import *


def process_type_file_9(column_type_data):

    volume_set = ' SET' in column_type_data
    volume_tester = 'TESTER' in column_type_data

    return {"volume_set": volume_set,
            "volume_tester": volume_tester}


def process_file_Lager(perfume_map: PerfumeMap, excel_file):

    print("File Lager.xlsx processing ... ")

    data = pd.read_excel(excel_file)
    data = data.iloc[:-1, :]

    # file_9 specificity
    # _3 -> Type
    # TYPE -> volume_tester, volume_set
    # _10 -> price

    perfume_list = [
        Perfume(
                str(perfume.BRAND),
                str(perfume.PRODUCT),
                str(perfume._3),
                make_sex_uniform(perfume.SEX),
                process_type_file_9(perfume.TYPE)["volume_tester"],
                process_type_file_9(perfume.TYPE)["volume_set"],
                perfume.SIZE,
                [perfume.DESCRIPTION],
                perfume._10,
                9)
        for perfume in data.itertuples()
    ]
    for p in perfume_list:
        perfume_map.insert_perfume(p)

    print("... finished")
