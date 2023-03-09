# import os 
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import norm

cwd = Path.cwd()
dir_main = Path.cwd().parent

def load_db(bool):
    if not bool:
        return None
    dir_full_db = f'{dir_main}/Data/YGO DB - export_full_db.csv'
    df = pd.read_csv(dir_full_db)
    df['Staple'].fillna('전용')
    for col in df.columns:
        if col != 'Code' and df[col].isnull().any():
            df[col].fillna(df['Code'], inplace=True)
    mean = df['Usage'].mean()
    std = df['Usage'].std()
    stdev = df['Usage'].apply(lambda x: round(norm.cdf(x, mean, std),2))
    df['SD'] = stdev
    return df

def add_sd(df):
    mean = df['Usage'].mean()
    std = df['Usage'].std()
    stdev = df['Usage'].apply(lambda x: round(norm.cdf(x, mean, std),2))
    df['SD'] = stdev
    return df

df = load_db(bool)
db_digit = np.asarray(df["Digit"])

def search_deck(deck_code):
    dir_deck_img = Path(dir_main).joinpath('deck')
    # create a dictionary of deck codes and file paths
    deck_paths = {file.stem: str(file) for file in dir_deck_img.glob('*')}
    # get the deck path for the given deck code
    deck_path = deck_paths.get(deck_code)
    # return the deck path, or None if the deck code is not found
    return deck_path


def search_digit(card_name, local):
    db_name = np.asarray(df[f"Name_{local.upper()}"])
    ind = np.where(db_name == card_name)[0][0]
    return db_digit [ind]

def search_name(digit, local):
    db_name = np.asarray(df[f"Name_{local.upper()}"])
    ind = np.where(db_digit == digit)[0][0]
    return db_name [ind]