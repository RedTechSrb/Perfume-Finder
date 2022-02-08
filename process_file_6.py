from Perfume import Perfume
from PerfumeMap import PerfumeMap

from utility import *


def process_naziv_file_6(column_Naziv_data):
    if pd.isna(column_Naziv_data):
        return {"description": None, "sex": None, "volume_amount": None}

    naziv_part_lists = column_Naziv_data.split(" / ")

    return {"description": naziv_part_lists[0], "sex": naziv_part_lists[2], "volume_amount": naziv_part_lists[1]}


def process_tip_file_6(column_Tip_data):
    volume_set = column_Tip_data == 'Set'
    volume_tester = column_Tip_data == 'Tester'

    if volume_set or volume_tester:
        volume_metadata = []
    else:
        volume_metadata = [column_Tip_data]

    return {"volume_set": volume_set, "volume_tester": volume_tester, "volume_metadata": volume_metadata}


def process_file_6(perfume_map: PerfumeMap, excel_file):
    data = pd.read_excel(excel_file)

    # (Naziv kreatora)_1 -> Brand
    # Naziv -> Description, volume_amount (Mililitraza has the same values), sex
    # Tip -> volume_set, volume_tester, volume_metadata
    # Cena -> Prince

    # for perfume in data.itertuples():
    #     print(str(perfume._1), " % ",
    #           str(process_naziv_file_6(perfume.Naziv)["description"]), " % ",
    #           str(None), " % ",
    #           make_sex_uniform(process_naziv_file_6(perfume.Naziv)["sex"]), " % ",
    #           process_tip_file_6(perfume.Tip)["volume_tester"], " % ",
    #           process_tip_file_6(perfume.Tip)["volume_set"], " % ",
    #           process_naziv_file_6(perfume.Naziv)["volume_amount"], " % ",
    #           process_tip_file_6(perfume.Tip)["volume_metadata"], " % ",
    #           perfume.Cena, " % ",
    #           6)

    perfume_list = [
        Perfume(str(perfume._1),
                str(process_naziv_file_6(perfume.Naziv)["description"]),
                str(None),
                make_sex_uniform(process_naziv_file_6(perfume.Naziv)["sex"]),
                process_tip_file_6(perfume.Tip)["volume_tester"],
                process_tip_file_6(perfume.Tip)["volume_set"],
                process_naziv_file_6(perfume.Naziv)["volume_amount"],
                process_tip_file_6(perfume.Tip)["volume_metadata"],
                perfume.Cena,
                6)
        for perfume in data.itertuples()
    ]
    for p in perfume_list:
        perfume_map.insert_perfume(p)
