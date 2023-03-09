import numpy as np
import pandas as pd
from pathlib import Path
import math
from util_db import load_db

cwd = Path.cwd()
dir_main = Path.cwd().parent

#######################################################

def dist(p1, p2):
    p1X, p1Y = p1
    p2X, p2Y = p2

    dX = (p2X - p1X) ** 2
    dY = (p2Y - p1Y) ** 2
    
    return dX + dY

# creates sorting mask funciton to sort points
def sort_pt(pts, sort_round):
    numb = int(math.log10(sort_round))+2
    sort_up = 10**numb
    ind_pt = []
    new_pt = []
    for i in range(len(pts)):
        ind_pt.append(i) # 0 1 2...
        nx = sort_round * math.ceil(pts[i][0]/sort_round)
        ny = sort_round * math.ceil(pts[i][1]/sort_round)
        new = nx + ny * sort_up
        new_pt.append(new)
    return [x for _, x in sorted(zip(new_pt, ind_pt))]

df = load_db(True)
db_digit = np.asarray(df["Digit"])
db_type = np.asarray(df["Type"])

#######################################################

# unpack card_loc / card_pos, digit_list data
def trans_raw ( card_loc, card_pos , digit_list):
    zip_digit = []
    zip_pt = []
    zip_pos = []
    for i in range(len(digit_list)):
        digit = digit_list[i]
        for j in range(len(card_loc[i])):
            coord = card_loc[i][j]
            pos = card_pos[i][j]
            # 01 Digit
            zip_digit.append(digit)
            # 01 Point
            zip_pt.append(coord)
            # 03 Pos
            zip_pos.append(pos)
    return zip_digit, zip_pt, zip_pos

def trans_dup (zip_pt, dup_tol) :
    dup_pt = list(zip_pt) #deepcopy(zip_pt)
    zip_ind = list(range(len(zip_pt)))
    dup_ind = []
    i=0
    while i< len(dup_pt):
        ind = [zip_ind[i]]
        j = len(dup_pt) -1
        while j > i:
            d = dist( dup_pt[i], dup_pt[j])
            if d < dup_tol **2 :
                dup_pt.pop(j)
                ind.append(zip_ind[j])
                zip_ind.pop(j)
            j = j- 1
        dup_ind.append(ind)
        i += 1
    return dup_pt, dup_ind

# def trans_group (dup_pt, zip_pt, zip_pos, zip_digit, dup_tol) :
#     group_pt = []
#     group_pos = []
#     group_digit = []
#     for i in range(len(dup_pt)):
#         pt_group = []
#         pos_group = []
#         digit_group = []
#         for j in range(len(zip_pt)):
#             d = dist(dup_pt[i], zip_pt[j])
#             if d < dup_tol**2:
#                 pt_group.append(zip_pt[j])
#                 pos_group.append(zip_pos[j])
#                 digit_group.append(zip_digit[j])
#         group_pt.append(pt_group)
#         group_pos.append(pos_group)
#         group_digit.append(digit_group)
#     return group_pt, group_pos, group_digit

def trans_group(dup_ind, zip_pt, zip_pos, zip_digit):
    group_pt = [[zip_pt[ind] for ind in sublist] for sublist in dup_ind]
    group_pos = [[zip_pos[ind] for ind in sublist] for sublist in dup_ind]
    group_digit = [[zip_digit[ind] for ind in sublist] for sublist in dup_ind]
    return group_pt, group_pos, group_digit

def trans_sort (group_pos, group_digit, group_pt, sort_round):
    pos_digit=[]
    pos_pt = []
    for i in range(len(group_pos)):
        digit = [x for _ , x in sorted(zip(group_pos[i],group_digit[i]), reverse=True)]
        pt = [x for _ , x in sorted(zip(group_pos[i],group_pt[i]), reverse=True)]
        pos_digit.append(digit[0])
        pos_pt.append(pt[0])
    sort_mask = sort_pt(pos_pt, sort_round)
    sort_digit = [pos_digit[i] for i in sort_mask]
    return sort_digit

def trans_name(sort_digit, local):
    sort_name = []
    for digit in sort_digit:
        ind = np.where(db_digit == int(digit))[0][0]
        name = np.asarray(df[f"Name_{local.upper()}"])[ind]
        sort_name.append(str(name))
    return sort_name

def trans_type(sort_digit):
    sort_type = []
    for digit in sort_digit:
        ind = np.where(db_digit == int(digit))[0][0]
        types = db_type[ind]
        sort_type.append(types)
    return sort_type

def find_consecutive_bounds(lst, val):
    bounds = []
    start = None
    for i in range(len(lst)):
        if lst[i] == val:
            if start is None:
                start = i
        else:
            if start is not None:
                bounds.append((start, i-1))
                start = None
    if start is not None:
        bounds.append((start, len(lst)-1))
    return bounds

def trans_paste(sort_name,sort_type,deck_code):
    deck_list = list(sort_name)
    token_ext = '엑스트라'
    if token_ext in sort_type:
    #######################################################
        # cons_pat = find_consecutive_bounds(sort_name, token_ext) #check for chunks
        # if len(cons_pat) > 1:
        #     print('side_extra')
        # else :
        #     cons_len = cons_pat[0][1] - cons_pat[0][0]
        #     print('good')
        #######################################################
        extra_ind = sort_type.index(token_ext)
        back_ind =  len(sort_type) - sort_type[::-1].index(token_ext) -1
        extra_len = back_ind - extra_ind +1
        #######################################################
        if extra_len < 15: # extend gap between side deck in case shorter
            for _ in range(15-extra_len):
                deck_list.insert(back_ind+1,"")
        if extra_ind < 60: # extend gap between main deck preventing leak
            for _ in range(60-extra_ind):
                deck_list.insert(extra_ind,"")
    deck_list.insert(0, deck_code)
    return deck_list