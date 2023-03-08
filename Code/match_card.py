import cv2
import numpy as np
# import imutils

# img_deck = cv2.imread(dir_deck)
# img_deck = imutils.resize(img_deck, width = deck_width)
# img_deck = cv2.cvtColor(img_deck, cv2.COLOR_BGR2GRAY)

# img_card = cv2.imread(dir_card, 0)
# img_card = imutils.resize(img_card, width = card_width)

def match_card(img_card, img_deck, threshold):
    res = cv2.matchTemplate(img_deck, img_card, cv2.TM_CCOEFF_NORMED)
    loc=np.where(res >= threshold)
    num_loc = tuple(zip(*loc[::-1]))
    num_pos = res[loc]

    # loc = np.argwhere(res >= threshold)
    # num_loc = loc.tolist()
    # num_pos = res[loc]

    return num_loc, num_pos


def match_card_v(img_card, img_deck, threshold):
    # card_loc = []
    # card_pos = []

    res = cv2.matchTemplate(img_deck, img_card, cv2.TM_CCOEFF_NORMED)
    loc=np.where(res >= threshold)

    num_loc = []
    for pt in zip(*loc[::-1]):
        num_loc.append(pt)
    # card_loc.append(num_loc)

    num_pos = res[loc]
    # num_pos = []
    # for i in range(len(loc[0])):
    #     u = loc[0][i]
    #     v = loc[1][i]
    #     pos = res[u][v]
    #     num_pos.append(pos)    
    # card_pos.append(num_pos)

    return num_loc, num_pos