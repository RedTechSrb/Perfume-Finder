from Perfume import Perfume
from PerfumeMap import PerfumeMap

from utility import *


def process_naziv_file_6(column_Naziv_data, column_Tip_data):
    if pd.isna(column_Naziv_data):
        return {"description": 'NAN', "sex": 'NAN', "volume_amount": 'NAN'}

    naziv_part_lists = column_Naziv_data.split(" / ")

    volume_tester = column_Tip_data == 'Tester'
    Description = naziv_part_lists[0]
    if 'TESTER' not in Description:
        if volume_tester:
            Description = Description + ' tester'

    return {"description": Description, "sex": naziv_part_lists[2], "volume_amount": naziv_part_lists[1]}


def process_tip_file_6(column_Tip_data):
    volume_set = column_Tip_data == 'Set'
    volume_tester = column_Tip_data == 'Tester'

    if volume_set or volume_tester:
        volume_metadata = []
    else:
        volume_metadata = [column_Tip_data]

    return {"volume_set": volume_set, "volume_tester": volume_tester, "volume_metadata": volume_metadata}


def process_file_V2(perfume_map: PerfumeMap, excel_file):

    print("File V2.xls processing ... ")

    data = pd.read_excel(excel_file)

    # (Naziv kreatora)_1 -> Brand
    # Naziv -> Description, volume_amount (Mililitraza has the same values), sex
    # Tip -> volume_set, volume_tester, volume_metadata
    # Cena -> Prince

    perfume_list = [
        Perfume(str(perfume._1),
                str(process_naziv_file_6(perfume.Naziv, perfume.Tip)["description"]),
                str('NAN'),
                make_sex_uniform(process_naziv_file_6(perfume.Naziv, perfume.Tip)["sex"]),
                process_tip_file_6(perfume.Tip)["volume_tester"],
                process_tip_file_6(perfume.Tip)["volume_set"],
                process_naziv_file_6(perfume.Naziv, perfume.Tip)["volume_amount"],
                process_tip_file_6(perfume.Tip)["volume_metadata"],
                perfume.Cena,
                6)
        for perfume in data.itertuples()
    ]
    for p in perfume_list:
        perfume_map.insert_perfume(p)

    print("... finished")
