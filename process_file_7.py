from Perfume import Perfume
from PerfumeMap import PerfumeMap

from utility import *


def process_group_file_7(column_group_data):
    volume_set = column_group_data == 'set'
    volume_tester = column_group_data == 'TESTER'

    if volume_set or volume_tester:
        volume_metadata = []
    else:
        volume_metadata = [column_group_data]

    return {"volume_set": volume_set, "volume_tester": volume_tester, "volume_metadata": volume_metadata}


def process_file_7(perfume_map: PerfumeMap, excel_file):

    print("File 7.xlsx processing ... ")

    data = pd.read_excel(excel_file)

    # BRANDS -> Brand
    # (ITEM DESCRIPTION)_3 -> Description
    # TYPE -> Type
    # SIZE -> volume_amount
    # PRICE -> Price
    # GROUP -> volume_set, volume_tester, volume_metadata

    perfume_list = [
        Perfume(str(perfume.BRANDS),
                str(perfume._3),
                str(perfume.TYPE),
                None,
                process_group_file_7(perfume.GROUP)["volume_tester"],
                process_group_file_7(perfume.GROUP)["volume_set"],
                make_ml_lowercase(perfume.SIZE),
                process_group_file_7(perfume.GROUP)["volume_metadata"],
                perfume.PIRCE,
                7)
        for perfume in data.itertuples()
    ]

    for p in perfume_list:
        perfume_map.insert_perfume(p)

    print("... finished")
