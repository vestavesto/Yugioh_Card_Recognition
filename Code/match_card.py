import cv2
import numpy as np
import imutils

def match_card(dir_card, dir_deck, deck_width, card_width, threshold):
    card_loc = []
    card_pos = []
    
    img_rgb = cv2.imread(dir_deck)
    img_rgb = imutils.resize(img_rgb, width = deck_width)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(dir_card, 0)
    template = imutils.resize(template, width = card_width)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc=np.where(res >= threshold)

    num_loc = []
    for pt in zip(*loc[::-1]):
        num_loc.append(pt)
    card_loc.append(num_loc)

    num_pos = []
    for i in range(len(loc[0])):
        u = loc[0][i]
        v = loc[1][i]
        pos = res[u][v]
        num_pos.append(pos)
    card_pos.append(num_pos)

    return card_loc, card_pos


def match_card_v(img_card, img_deck, threshold):
    card_loc = []
    card_pos = []

    res = cv2.matchTemplate(img_deck, img_card, cv2.TM_CCOEFF_NORMED)
    loc=np.where(res >= threshold)

    num_loc = []
    for pt in zip(*loc[::-1]):
        num_loc.append(pt)
    card_loc.append(num_loc)

    num_pos = []
    for i in range(len(loc[0])):
        u = loc[0][i]
        v = loc[1][i]
        pos = res[u][v]
        num_pos.append(pos)
    card_pos.append(num_pos)

    return card_loc, card_pos