class Perfume:

    def __init__(self, brand, description, perfume_type, sex, volume_tester, volume_set, volume_amount, volume_metadata,
                 price, parent_file):
        self.brand = brand
        self.description = description
        self.perfume_type = perfume_type
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

    def get_price(self):
        return self.price

    def __str__(self) -> str:
        return f"Perfume[{self.parent_file}] ({self.brand}, {self.description}, {self.perfume_type}, {self.sex}, \
                {self.volume_tester}, {self.volume_set}, {self.volume_amount}, {self.volume_metadata}) -> {self.price}"
