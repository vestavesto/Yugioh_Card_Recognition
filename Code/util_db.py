import os 
import numpy as np
import pandas as pd
from pathlib import Path

cwd = Path.cwd()
dir_main = Path.cwd().parent

dir_full_db = f'{dir_main}/Data/YGO DB - export_full_db.csv'
df = pd.read_csv(dir_full_db)
def fill_na_with_code(df):
    for col in df.columns:
        if col != 'Code' and df[col].isnull().any():
            df[col].fillna(df['Code'], inplace=True)
    return df
fill_na_with_code(df)
db_digit = np.asarray(df["Digit"])
db_name_ko = np.asarray(df["Name_KO"])
db_type = np.asarray(df["Type"])

def search_deck(deck_code):
    dir_deck_img = f'{dir_main}/deck'
    deck_img_list = os.listdir(dir_deck_img)
    deck_code_list = [os.path.splitext(filename)[0] for filename in deck_img_list]
    deck_code_ind = deck_code_list.index(deck_code)
    deck_path = deck_img_list[deck_code_ind]
    return f'{dir_main}/deck/{deck_path}'


def search_card(card_name):
    ind = np.where(db_name_ko == card_name)[0][0]
    return db_digit [ind]