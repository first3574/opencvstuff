#!/usr/env python
import numpy as np
import cv2
import time

def read_color_values():
    with open('static/colorvalues') as cvf:
        hl, sl, vl = cvf.readline().split(',')
        hh, sh, vh = cvf.readline().split(',')
    return [int(hl), int(sl), int(vl)], [int(hh), int(sh), int(vh)]

def save_color_values(hl, sl, vl, hh, sh, vh):
    with open('static/colorvalues', 'w') as cvf:
        cvf.write('{},{},{}\n'.format(hl, sl, vl))
        cvf.write('{},{},{}\n'.format(hh, sh, vh))


def get_yellow_frame(cap, lowvals, highvals):
    _, frame = cap.read()

    # Our operations on the frame come here
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # yellow color range
    lower_yellow = np.array(lowvals)
    upper_yellow = np.array(highvals)
    # Threshold the HSV image to get only yellow colors
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    return mask 

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    lowvals, highvals = read_color_values()
    print(lowvals)
    print(highvals)
    mask = get_yellow_frame(cap, lowvals, highvals)
    cv2.imwrite("static/tempcalibrate.png", mask )

