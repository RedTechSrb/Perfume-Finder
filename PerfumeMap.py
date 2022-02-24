import Perfume


class PerfumeMap:

    def __init__(self):
        self.perfume_map = {}

    def insert_perfume(self, perfume: Perfume):
        new_python_key = perfume.get_minimal()

        # TODO: add volume
        if new_python_key == ('NAN', 'NAN', 'NAN'):
            return

        for key, value in self.perfume_map.items():
            if key == new_python_key:
                self.perfume_map[key].append(perfume)
                return

        self.perfume_map[new_python_key] = [perfume]

    def __str__(self) -> str:

        map_string = ""

        for key, value in self.perfume_map.items():
            map_string += str(key)
            map_string += " -> "
            map_string += str(value)
            map_string += "\n"

        return map_string

    def get_map(self):
        return self.perfume_map

    def get_minimal_price(self, key):
        return min(list(map(lambda p: p.get_price(), self.perfume_map[key])))
