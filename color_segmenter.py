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

# ---------------------------------------------------
# Global Variables
# ---------------------------------------------------
min_BH = 0
max_BH = 255
min_GS = 0
max_GS = 255
min_RV = 0
max_RV = 255


# Define functions of trackbars
def minOnTrackbarBH(threshold):
    """
    Trackbar for the minimum threshold for the Blue (RGB) or Hue (HSV) channel
    :param threshold: the threshold for the channel in question. Datatype: int
    """
    global min_BH
    min_BH = threshold
    print('Selected threshold ' + str(min_BH) + ' for limit min B/H')


def maxOnTrackbarBH(threshold):
    """
    Trackbar for the maximum threshold for the Blue (RGB) or Hue (HSV) channel
    :param threshold: the threshold for the channel in question. Datatype: int
    """
    global max_BH
    max_BH = threshold
    print('Selected threshold ' + str(max_BH) + ' for limit max B/H')


def minOnTrackbarGS(threshold):
    """
    Trackbar for the minimum threshold for the Green (RGB) or Saturation (HSV) channel
    :param threshold: the threshold for the channel in question. Datatype: int
    """
    global min_GS
    min_GS = threshold
    print('Selected threshold ' + str(min_GS) + ' for limit min G/S')


def maxOnTrackbarGS(threshold):
    """
    Trackbar for the maximum threshold for the Green (RGB) or Saturation (HSV) channel
    :param threshold: the threshold for the channel in question. Datatype: int
    """
    global max_GS
    max_GS = threshold
    print('Selected threshold ' + str(max_GS) + ' for limit max G/S')


def minOnTrackbarRV(threshold):
    """
    Trackbar for the minimum threshold for the Red (RGB) or Value (HSV) channel
    :param threshold: the threshold for the channel in question. Datatype: int
    """
    global min_RV
    min_RV = threshold
    print('Selected threshold ' + str(min_RV) + ' for limit min R/V')


def maxOnTrackbarRV(threshold):
    """
    Trackbar for the maximum threshold for the Red (RGB) or Value (HSV) channel
    :param threshold: the threshold for the channel in question. Datatype: int
    """
    global max_RV
    max_RV = threshold
    print('Selected threshold ' + str(max_RV) + ' for limit max R/V')


def main():
    window_name = 'window - Ex3a'
    cv2.namedWindow(window_name)
    capture = cv2.VideoCapture(0)
    #capture.set(cv2.CAP_PROP_FPS, 15)

    cv2.createTrackbar('min B', window_name, 0, 255, minOnTrackbarBH)
    cv2.createTrackbar('max B', window_name, 255, 255, maxOnTrackbarBH)
    cv2.createTrackbar('min G', window_name, 0, 255, minOnTrackbarGS)
    cv2.createTrackbar('max G', window_name, 255, 255, maxOnTrackbarGS)
    cv2.createTrackbar('min R', window_name, 0, 255, minOnTrackbarRV)
    cv2.createTrackbar('max R', window_name, 255, 255, maxOnTrackbarRV)

    # Set the trackbar position to 255 for maximum trackbars
    cv2.setTrackbarPos('max B', window_name, 255)
    cv2.setTrackbarPos('max G', window_name, 255)
    cv2.setTrackbarPos('max R', window_name, 255)

    # Initialize trackbars
    minOnTrackbarBH(0)
    maxOnTrackbarBH(255)
    minOnTrackbarGS(0)
    maxOnTrackbarGS(255)
    minOnTrackbarRV(0)
    maxOnTrackbarRV(255)

    while True:
        _, image = capture.read()

        ranges = {'limits': {'B': {'min': min_BH, 'max': max_BH},
                            'G': {'min': min_GS, 'max': max_GS},
                            'R': {'min': min_RV, 'max': max_RV}}}

        # Convert the dict structure created before to numpy arrays, because opencv uses it.
        mins = np.array([ranges['limits']['B']['min'], ranges['limits']['G']['min'], ranges['limits']['R']['min']])
        maxs = np.array([ranges['limits']['B']['max'], ranges['limits']['G']['max'], ranges['limits']['R']['max']])

        segmented = cv2.inRange(image, mins, maxs)

        cv2.imshow('Original', image)
        cv2.imshow(window_name, segmented)

        if cv2.waitKey(1) == ord('w'):
            file_name = 'limits.json'
            with open(file_name, 'w') as file_handle:
                print('writing dictionary ranges to file ' + file_name)
                json.dump(ranges, file_handle)  # d is the dictionaryqqqqqqqqq

        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == '__main__':
    main()
