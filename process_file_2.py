from re import match

from Perfume import Perfume
from PerfumeMap import PerfumeMap

from utility import *


def process_volume_file_2(volume):
    if pd.isna(volume):
        return {"volume_set": None, "volume_tester": None, "volume_amount": None, "volume_metadata": None}

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

    # file_2 specificity
    # Volume -> volume_set, volume_tester, volume_amount, volume_metadata
    # (Net EUR)_7 -> price

    perfume_list = [
        Perfume(str(perfume.Brand),
                str(perfume.Description),
                str(perfume.Type),
                make_sex_uniform(perfume.Sex),
                process_volume_file_2(perfume.Volume)["volume_tester"],
                process_volume_file_2(perfume.Volume)["volume_set"],
                process_volume_file_2(perfume.Volume)["volume_amount"],
                process_volume_file_2(perfume.Volume)["volume_metadata"],
                perfume._7,
                2)
        for perfume in data.itertuples()
    ]

    for p in perfume_list:
        perfume_map.insert_perfume(p)
