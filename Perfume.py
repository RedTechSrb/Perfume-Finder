class Perfume:

    def __init__(self, brand, description, perfume_type, sex, volume_tester, volume_set, volume_amount, volume_metadata,
                 price, parent_file):
        self.brand = " ".join(brand.upper().split())
        self.description = " ".join(description.upper().split())
        self.perfume_type = perfume_type.upper()
        self.sex = sex
        self.volume_tester = volume_tester
        self.volume_set = volume_set
        self.volume_amount = volume_amount
        self.volume_metadata = volume_metadata
        self.price = price
        self.parent_file = parent_file

    def get_description(self):
        return self.brand, self.description, self.perfume_type, self.sex, self.volume_tester, self.volume_set, \
               self.volume_amount

    def get_minimal(self):
        # TODO: add volume
        return self.brand, self.description

    def get_parent_file(self):
        return self.parent_file

    def get_price(self):
        return self.price

    def __str__(self) -> str:
        return f"Perfume[{self.parent_file}] ({self.brand}, {self.description}, {self.perfume_type}, {self.sex}," + \
               f" {self.volume_tester}, {self.volume_set}, {self.volume_amount}, {self.volume_metadata})" + \
               f" -> {self.price}"
