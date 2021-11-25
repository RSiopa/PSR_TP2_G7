#!/usr/bin/env python3
# --------------------------------------------------
# Python script for color adjustment and saving the values to a json file.
# Rafael Inacio Siopa.
# Rodrigo Dinis Martins Ferreira.
# Bartosz Bartosik.
# PSR, November 2021.
# --------------------------------------------------
import json
import cv2
import numpy as np
from colorama import Fore, Style

# trackbar callback function that is not used
def nothing(x):
    pass


def main():

    # -----------------------------------------------------------
    # Initialization
    # -----------------------------------------------------------

    print("\nWelcome to our color segmenter program. \n\nContributors: \n- Rafael Inacio Siopa \n- Rodrigo Dinis Martins Ferreira "
          " \n- Bartosz Bartosik \n\nPSR, University of Aveiro, "
          "November 2021.\n")

    # Name of the window used to show the segmented image
    window_name = 'Segmented'

    # Create a window with the name of the window_name variable
    cv2.namedWindow(window_name)

    # Capture a frame of the webcam
    capture = cv2.VideoCapture(0)

    # Dictionary where the values of the segmentation are stored
    ranges = {'limits': {'B': {'max': 255, 'min': 0},
                         'G': {'max': 255, 'min': 0},
                         'R': {'max': 255, 'min': 0}}}

    # Creation of all the 6 trackbars
    cv2.createTrackbar('min B', window_name, 0, 255, nothing)
    cv2.createTrackbar('max B', window_name, 255, 255, nothing)
    cv2.createTrackbar('min G', window_name, 0, 255, nothing)
    cv2.createTrackbar('max G', window_name, 255, 255, nothing)
    cv2.createTrackbar('min R', window_name, 0, 255, nothing)
    cv2.createTrackbar('max R', window_name, 255, 255, nothing)

    print("\nPress " + Fore.GREEN + "w" + Style.RESET_ALL + " to save the trackbars limits.")
    print("Press " + Fore.GREEN + "q" + Style.RESET_ALL + " to to quit the program")

    # -----------------------------------------------------------
    # Continuous Operation
    # -----------------------------------------------------------

    while True:
        # Variable image has the realtime webcam video
        _, image = capture.read()

        # Create an array and update it with the min and max of the trackbars' limits for the inRange function
        mins = np.array([ranges['limits']['B']['min'], ranges['limits']['G']['min'], ranges['limits']['R']['min']])
        maxs = np.array([ranges['limits']['B']['max'], ranges['limits']['G']['max'], ranges['limits']['R']['max']])

        # When a trackbar is moved, the values are stored in the dictionary ranges
        ranges['limits']['B']['min'] = mins[0] = cv2.getTrackbarPos('min B', window_name)
        ranges['limits']['G']['min'] = mins[1] = cv2.getTrackbarPos('min G', window_name)
        ranges['limits']['R']['min'] = mins[2] = cv2.getTrackbarPos('min R', window_name)
        ranges['limits']['B']['max'] = maxs[0] = cv2.getTrackbarPos('max B', window_name)
        ranges['limits']['G']['max'] = maxs[1] = cv2.getTrackbarPos('max G', window_name)
        ranges['limits']['R']['max'] = maxs[2] = cv2.getTrackbarPos('max R', window_name)

        # Segment the webcam image in function of the limits of the trackbars
        segmented = cv2.inRange(image, mins, maxs)

        # Show the segmented image and the webcam video stream
        cv2.imshow(window_name, segmented)
        cv2.imshow('Original', image)

        # Saves key pressed
        key = cv2.waitKey(20)

        # If the pressed key is 'w', the limits of the trackbars are saved in limits.json file
        if key == ord('w'):
            file_name = 'limits.json'
            with open(file_name, 'w') as file_handle:
                print('Writing dictionary ranges to file ' + file_name)
                json.dump(ranges, file_handle)  # ranges is the dictionary

        # If the pressed key is 'q', the program ends
        if key == ord('q'):
            break


if __name__ == '__main__':
    main()
