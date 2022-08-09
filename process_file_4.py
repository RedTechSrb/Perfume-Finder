from Perfume import Perfume
from PerfumeMap import PerfumeMap

from utility import *

def process_type_file_4(column_Type_data):
    if pd.isna(column_Type_data):
        return {"volume_set": 'NAN', "volume_tester": 'NAN', "volume_metadata": 'NAN'}

    type_part_lists = column_Type_data.split()
    volume_set = 'SET' in type_part_lists
    volume_tester = 'Tester' in type_part_lists

    volume_metadata = list(filter(lambda v: (v != 'SET' and v != 'Tester'), type_part_lists))

    return {"volume_set": volume_set, "volume_tester": volume_tester, "volume_metadata": volume_metadata}


def process_file_4(perfume_map: PerfumeMap, excel_file):

    print("File 4.xlsx processing ... ")

    data = pd.read_excel(excel_file, skiprows=[0, 1])

    # file_4 specificity
    # _9 -> Price

    perfume_list = [
        Perfume(str(perfume.Brand),
                str(perfume.Description),
                'NAN',
                make_sex_uniform(perfume.Sex),
                process_type_file_4(str(perfume.Type))["volume_tester"],
                process_type_file_4(str(perfume.Type))["volume_set"],
                nan_to_none(perfume.Size),
                process_type_file_4(str(perfume.Type))["volume_metadata"],
                perfume._9,
                4)
        for perfume in data.itertuples()
    ]

    for p in perfume_list:
        perfume_map.insert_perfume(p)

    print("... finished")
