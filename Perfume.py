class Perfume:

    def __init__(self, brand, description, perfume_type, sex, volume_type, volume_set, volume_amount, price,
                 parent_file):
        self.brand = brand
        self.description = description
        self.perfume_type = perfume_type
        self.sex = sex
        self.volume_type = volume_type
        self.volume_set = volume_set
        self.volume_amount = volume_amount
        self.price = price
        self.parent_file = parent_file

    def get_description(self):
        return self.brand, self.description, self.perfume_type, self.sex, self.volume_type, self.volume_set, \
               self.volume_amount

    def get_price(self):
        return self.price

    def __str__(self) -> str:
        return f"Perfume[{self.parent_file}] ({self.brand}, {self.description}, {self.perfume_type}, {self.sex}, {self.volume_type}, {self.volume_set}, {self.volume_amount}) -> {self.price}"
