# Code from https://github.com/bnsreenu/python_for_microscopists/blob/05bf7ea369bf19ef8c5b1d3f9b78ebd125db763c/Tips_Tricks_25_locating_objects_in_large_images_via_template_matching.py

import cv2
import numpy as np
import imutils

def match_scale(dir_card, dir_deck, deck_width):
    img_deck = cv2.imread(dir_deck)
    img_deck = imutils.resize(img_deck, width = deck_width)
    img_gray = cv2.cvtColor(img_deck, cv2.COLOR_BGR2GRAY)
    
    img_card = cv2.imread(dir_card, 0)

    best_match = None
    sc1 = int((deck_width / 10) * 0.8 )
    sc2 = int((deck_width / 10) * 1.1 )
    sc_dif = abs(sc2-sc1)+1

    for scale in np.linspace(sc1, sc2, sc_dif):
        resized_img_card = imutils.resize(img_card, width = int(scale))    
        res = cv2.matchTemplate(img_gray, resized_img_card, cv2.TM_SQDIFF) #min_val, max_val, min_loc, max_loc
        min_val, _, min_loc, _ = cv2.minMaxLoc(res)

        if best_match is None or min_val <= best_match[0]:
            ideal_scale=scale 
            best_match = [min_val, min_loc, ideal_scale]

    # ideal_w = int(img_card.shape[1]*ideal_scale / img_card.shape[0])
    # ideal_h = int(ideal_scale)
    # print(f"Ideal card image size is : {ideal_w} x {ideal_h}")

    return int(ideal_scale)


def match_scale_mp_v(dir_card, dir_deck, deck_width, threshold):
    img_deck = cv2.imread(dir_deck)
    img_deck = imutils.resize(img_deck, width = deck_width)
    img_gray = cv2.cvtColor(img_deck, cv2.COLOR_BGR2GRAY)
    img_card = cv2.imread(dir_card, 0)

    best_match = None
    sc1 = int((deck_width / 10) * 0.8 )
    sc2 = int((deck_width / 10) * 1.1 )
    sc_dif = abs(sc2-sc1)+1
    for scale in np.linspace(sc1, sc2, sc_dif):
        resized_img_card = imutils.resize(img_card, width = int(scale))    
        res = cv2.matchTemplate(img_gray, resized_img_card, cv2.TM_SQDIFF) #min_val, max_val, min_loc, max_loc
        min_val, _, min_loc, _ = cv2.minMaxLoc(res)
        if best_match is None or min_val <= best_match[0]:
            ideal_scale=scale 
            best_match = [min_val, min_loc, ideal_scale]

    card_width = int(ideal_scale)

    # img_card = cv2.imread(dir_card, 0)
    img_card = imutils.resize(img_card, width = card_width)
    res = cv2.matchTemplate(img_gray, img_card, cv2.TM_CCOEFF_NORMED)
    loc=np.where(res >= threshold)

    lengths = [len(elem) for elem in loc]

    if all(length == 0 for length in lengths):
        actual_length = 0
    else:
        actual_length = max(lengths)

    if actual_length >0 :
        real_width = card_width 
    else :
        real_width = None
    
    return real_width


def match_scale_mp(img_card, img_deck, card_min, card_max, step, threshold):

    best_match = None
    for scale in np.linspace(card_min, card_max, step):
        resized_img_card = imutils.resize(img_card, width = int(scale))    
        res = cv2.matchTemplate(img_deck, resized_img_card, cv2.TM_SQDIFF) #min_val, max_val, min_loc, max_loc
        min_val, _, min_loc, _ = cv2.minMaxLoc(res)
        if best_match is None or min_val <= best_match[0]:
            ideal_scale=scale 
            best_match = [min_val, min_loc, ideal_scale]

    card_width = int(ideal_scale)

    img_card = imutils.resize(img_card, width = card_width)
    res = cv2.matchTemplate(img_deck, img_card, cv2.TM_CCOEFF_NORMED)
    loc=np.where(res >= threshold)

    lengths = [len(elem) for elem in loc]

    if all(length == 0 for length in lengths):
        actual_length = 0
    else:
        actual_length = max(lengths)

    if actual_length >0 :
        real_width = card_width 
    else :
        real_width = None
    
    return real_width