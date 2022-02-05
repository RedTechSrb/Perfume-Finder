import pandas as pd


def make_sex_uniform(sex):
    if pd.isna(sex):
        return None
    sex = sex.upper()
    if sex == "MEN":
        return "M"
    elif sex == "MAN":
        return "M"
    elif sex == "MUŠKI":
        return "M"
    elif sex == "WOMEN":
        return "W"
    elif sex == "WOMAN":
        return "W"
    elif sex == "ŽENSKI":
        return "W"
    elif sex == "UNISEX":
        return "U"
    else:
        return "U"


def nan_to_none(variable):
    if pd.isna(variable):
        return None
    return variable
