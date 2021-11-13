#!/usr/bin/python3.8
# --------------------------------------------------
# Python script for color adjustment and saving the values to a json file.
# Rafael Inacio Siopa.
# Frederico Ribeiro e Martins.
# Rodrigo Dinis Martins Ferreira.
# Bartosz Bartosik.
# PSR, November 2021.
# --------------------------------------------------
import json
import cv2
import numpy as np


def nothing(x):
    pass


def main():
    window_name = 'window - Ex3a'
    cv2.namedWindow(window_name)
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FPS, 15)

    ranges = {'limits': {'B': {'max': 255, 'min': 0},
                         'G': {'max': 255, 'min': 0},
                         'R': {'max': 255, 'min': 0}}}

    cv2.createTrackbar('min B', window_name, 0, 255, nothing)
    cv2.createTrackbar('max B', window_name, 255, 255, nothing)
    cv2.createTrackbar('min G', window_name, 0, 255, nothing)
    cv2.createTrackbar('max G', window_name, 255, 255, nothing)
    cv2.createTrackbar('min R', window_name, 0, 255, nothing)
    cv2.createTrackbar('max R', window_name, 255, 255, nothing)

    while True:
        _, image = capture.read()

        mins = np.array([ranges['limits']['B']['min'], ranges['limits']['G']['min'], ranges['limits']['R']['min']])
        maxs = np.array([ranges['limits']['B']['max'], ranges['limits']['G']['max'], ranges['limits']['R']['max']])

        ranges['limits']['B']['min'] = mins[0] = cv2.getTrackbarPos('min B', window_name)
        ranges['limits']['G']['min'] = mins[1] = cv2.getTrackbarPos('min G', window_name)
        ranges['limits']['R']['min'] = mins[2] = cv2.getTrackbarPos('min R', window_name)
        ranges['limits']['B']['max'] = maxs[0] = cv2.getTrackbarPos('max B', window_name)
        ranges['limits']['G']['max'] = maxs[1] = cv2.getTrackbarPos('max G', window_name)
        ranges['limits']['R']['max'] = maxs[2] = cv2.getTrackbarPos('max R', window_name)

        mask_black = cv2.inRange(image, mins, maxs)
        cv2.imshow(window_name, mask_black)

        if cv2.waitKey(1) == ord('w'):
            file_name = 'limits.json'
            with open(file_name, 'w') as file_handle:
                print('writing dictionary ranges to file ' + file_name)
                json.dump(ranges, file_handle)  # d is the dictionary

        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == '__main__':
    main()
