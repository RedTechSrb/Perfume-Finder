import os

from process_file_2 import *
from process_file_3 import *
from process_file_4 import *
from process_file_5 import *
from process_file_6 import *
from process_file_7 import *


def main():
    root_folder = "data"
    perfume_map1 = PerfumeMap()
    perfume_map2 = PerfumeMap()
    perfume_map = PerfumeMap()
    for root, dirs, files in os.walk(root_folder):
        for filename in files:

            if filename == "2.xlsx":
                process_file_2(perfume_map, os.path.join(root, filename))
            elif filename == "3.xlsx":
                process_file_3(perfume_map, os.path.join(root, filename))
            elif filename == "4.xlsx":
                process_file_4(perfume_map, os.path.join(root, filename))
            elif filename == "5.xlsx":
                process_file_5(perfume_map, os.path.join(root, filename))
            elif filename == "6.xls":
                process_file_6(perfume_map, os.path.join(root, filename))
            elif filename == "7.xlsx":
                process_file_7(perfume_map, os.path.join(root, filename))

    for p in perfume_map.get_map()[('CD',
                                    'DIOR HOMME')]:
        print(p)
    print()

    for p in perfume_map.get_map()[('CHRISTIAN DIOR',
                                    'DIOR HOMME')]:
        print(p)
    print()

    for p in perfume_map.get_map()[('CHRISTIAN DIOR',
                                    'DIOR HOMME INTENSE')]:
        print(p)
    print()

    for p in perfume_map.get_map()[('CHRISTIAN DIOR',
                                    'DIOR HOMME EDT')]:
        print(p)
    print()


if __name__ == "__main__":
    main()
