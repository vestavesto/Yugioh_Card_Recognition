import os 
import numpy as np
import pandas as pd
from pathlib import Path

cwd = Path.cwd()
dir_main = Path.cwd().parent

dir_full_db = f'{dir_main}/Data/full_db.txt'
df = pd.read_csv(dir_full_db, sep='\t')

def fill_na_with_code(df):
    for col in df.columns:
        if col != 'Code' and df[col].isnull().any():
            df[col].fillna(df['Code'], inplace=True)
    return df
fill_na_with_code(df)

db_digit = np.asarray(df["Digit"])
db_name_ko = np.asarray(df["Name_KO"])

# def search_deck (deck_sample):
#     dir_deck_pool = f'{dir_main}/Deck/'
#     deck_pool = os.listdir(dir_deck_pool)

#     ind_deck = []
#     for deck in deck_pool:
#         deck_txt = deck.split(".")[0]
#         deck_txt = deck_txt.split("(")[0]
#         deck_number = int(deck_txt.replace("-","0"))
#         ind_deck.append(deck_number)
#     deck_sorted = [x for _,x in sorted(zip(ind_deck,deck_pool))]

#     return f'{dir_deck_pool}{deck_sorted[deck_sample]}'


def search_deck (deck_code):
    dir_deck_img = f'{dir_main}/deck'
    deck_img_list = os.listdir(dir_deck_img)
    deck_code_list = [os.path.splitext(filename)[0] for filename in deck_img_list]
    deck_code_ind = deck_code_list.index(deck_code)
    deck_path = deck_img_list[deck_code_ind]
    dir_deck = f'{dir_main}/deck/{deck_path}'
    return dir_deck


def search_card(card_name):
    ind = np.where(db_name_ko == card_name)[0][0]
    digit = db_digit [ind]
    return digit