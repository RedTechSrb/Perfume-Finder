import Perfume


class PerfumeMap:

    def __init__(self):
        self.perfume_map = {}

    def insert_perfume(self, perfume: Perfume):
        key = perfume.get_description()

        if key in self.perfume_map.keys():
            self.perfume_map[key].append((perfume.get_parent_file(), perfume.get_price()))
        else:
            self.perfume_map[key] = [(perfume.get_parent_file(), perfume.get_price())]

    def __str__(self) -> str:

        map_string = ""

        for key, value in self.perfume_map.items():
            map_string += str(key)
            map_string += " -> "
            map_string += str(value)
            map_string += "\n"

        return map_string


