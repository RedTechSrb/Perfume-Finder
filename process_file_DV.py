import re
from re import match

from Perfume import Perfume
from PerfumeMap import PerfumeMap

from utility import *


def fix_volume_file_10(raw_volume):
    volume = raw_volume.replace(',', '.')
    volume = volume.replace('g', 'ml')
    volume = volume.replace('pcs', 'ml')
    return volume


def process_Description_Note_file_10(column_Description_data, column_note_data):

    Description = column_Description_data

    volume_set = 'set' in nan_to_none(column_note_data)

    perfume_type_search = 'edp' in column_Description_data
    perfume_type = 'NAN'
    if perfume_type_search:
        perfume_type = 'edp'

    perfume_type_search = 'edt' in column_Description_data
    if perfume_type_search:
        perfume_type = 'edt'

    perfume_type_search = 'edc' in column_Description_data
    if perfume_type_search:
        perfume_type = 'edc'


    volume_search = re.search('^(.*)(  *\d*ml|  *\d+\,\d+ml|  *\d+\.\d+ml|\d\d\dml|  *\d+\.\d+g|  *\d+\,\d+g|  *\d*g|\d\d\dg|  *\d*pcs) *(.*)$', column_Description_data, re.IGNORECASE)
    volume = 'NAN'

    if volume_search:
        volume = volume_search.group(2)

        if not volume_set:
            Description = Description.replace(volume, '')

        volume = fix_volume_file_10(volume)
        volume = volume.replace(' ', '')

    return {"Description": Description,
            "perfume_type": perfume_type,
            "volume_amount": volume,
            "volume_set": volume_set,
            "volume_tester": 'tstr' in column_Description_data}


def process_file_DV(perfume_map: PerfumeMap, excel_file):

    print("File DV.xls processing ... ")

    data = pd.read_excel(excel_file)

    # _1 -> Brand
    # Description -> Description, perfume_type, volume_tester, volume_set, volume_amount
    # Note -> set
    # euro -> Price

    perfume_list = [
        Perfume(
            str(perfume._1),
            process_Description_Note_file_10(perfume.Description, perfume.Note)["Description"],
            process_Description_Note_file_10(perfume.Description, perfume.Note)["perfume_type"],
            make_sex_uniform(perfume.Sex),
            process_Description_Note_file_10(perfume.Description, perfume.Note)["volume_tester"],
            process_Description_Note_file_10(perfume.Description, perfume.Note)["volume_set"],
            process_Description_Note_file_10(perfume.Description, perfume.Note)["volume_amount"],
            [],
            perfume.euro,
            10)
        for perfume in data.itertuples()
    ]
    for p in perfume_list:
        perfume_map.insert_perfume(p)

    print("... finished")
