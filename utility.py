import pandas as pd


def make_sex_uniform(sex):
    if pd.isna(sex):
        return 'NAN'
    sex = sex.upper()
    if sex == "MEN":
        return "M"
    elif sex == "MAN":
        return "M"
    elif sex == "M":
        return "M"
    elif sex == "MUSKI":
        return "M"
    elif sex == "MUŠKI":
        return "M"
    elif sex == "WOMEN":
        return "W"
    elif sex == "W":
        return "W"
    elif sex == "WOMAN":
        return "W"
    elif sex == "ZENSKI":
        return "W"
    elif sex == "ŽENSKI":
        return "W"
    elif sex == "UNISEX":
        return "U"
    elif sex == "U":
        return "U"
    else:
        return "NEPOZNATO"


def nan_to_none(variable):
    if pd.isna(variable):
        return 'NAN'
    return variable


def make_ml_lowercase(volume):
    if pd.isna(volume):
        return 'NAN'
    return volume[0:-2] + volume[-2:].lower()


def map_file_number_to_filename(filenumber: int):
    if filenumber == 2:
        return "ALL.xlsx"
    elif filenumber == 3:
        return "LUCAS.xlsx"
    elif filenumber == 4:
        return "KULD.xlsx"
    elif filenumber == 5:
        return "LILI.xlsx"
    elif filenumber == 6:
        return "V2.xls"
    elif filenumber == 7:
        return "DDP.xlsx"
    elif filenumber == 8:
        return "D1.xls"
    elif filenumber == 9:
        return "Lager.xlsx"
