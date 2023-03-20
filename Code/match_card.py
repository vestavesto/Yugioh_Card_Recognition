import cv2
import numpy as np
import imutils

def match_card(img_card, img_deck, threshold):
    res = cv2.matchTemplate(img_deck, img_card, cv2.TM_CCOEFF_NORMED)
    loc=np.where(res >= threshold)
    num_loc = tuple(zip(*loc[::-1]))
    num_pos = res[loc]

    return num_loc, num_pos


def match_card_legacy(dir_card, dir_deck, deck_width, threshold):
    img_card = cv2.imread(dir_card, 0)

    img_deck = cv2.imread(dir_deck)
    img_deck = imutils.resize(img_deck, width = deck_width)
    img_deck = cv2.cvtColor(img_deck, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(img_deck, img_card, cv2.TM_CCOEFF_NORMED)
    loc=np.where(res >= threshold)

    num_loc = tuple(zip(*loc[::-1]))
    num_pos = res[loc]

    return num_loc, num_pos