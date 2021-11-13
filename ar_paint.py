#!/usr/bin/python3.8
# --------------------------------------------------
# Python script with a variety of painting functions!
# Rafael Inacio Siopa.
# Rodrigo Dinis Martins Ferreira.
# Frederico Ribeiro e Martins.
# Bartosz Bartosik.
# PSR, November 2021.
# --------------------------------------------------
import argparse
import copy
from numpy import zeros
from color_segmenter import *

# Argument
parser = argparse.ArgumentParser(description='Definition of test mode')
parser.add_argument('-j', '--json', type=str, help='Full path to json file.\n ')
args = vars(parser.parse_args())


def main():

    # -----------------------------------------------------------
    # Initialization
    # -----------------------------------------------------------

    # Read dictionary in Json file
    data = json.load(open(args['json']))
    limits = data['limits']

    # Video capture setup
    window_name = 'window_sketch'
    cv2.namedWindow(window_name)
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FPS, 15)

    # White image aka image_sketch created
    _, image = capture.read()
    h = len(image)
    w = len(image[0])
    image_sketch = zeros([h, w, 3])

    for y in range(h):
        for x in range(w):
            image_sketch[y, x] = [255, 255, 255]

    # Mins and maxs acquired from dictionary in Json file
    mins = np.array([limits['B']['min'], limits['G']['min'], limits['R']['min']])
    maxs = np.array([limits['B']['max'], limits['G']['max'], limits['R']['max']])

    # Variable for when cv2.connectedComponentsWithStats is used (can be 8 too)
    connectivity = 4

    # Flag for the program to know that the user just started to draw a new line (lines can be disconnected)
    flag_newline = 1

    # -----------------------------------------------------------
    # Continuous Operation
    # -----------------------------------------------------------

    while True:
        _, image = capture.read()
        image_origin = copy.copy(image)
        # Mask gotten from mins and maxs
        mask = cv2.inRange(image_origin, mins, maxs)
        # Initiation of mask for only the largest object (needed here in case the program detects no items at the start)
        mask_largest = np.zeros(mask.shape)

        # Gets number of components, stats and their centroids
        nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity, cv2.CV_32S)
        sizes = stats[1:, -1]
        nb_components = nb_components - 1
        min_size = 0
        for i in range(0, nb_components):
            # Goes through all the objects but only paints and gets centroid of the largest
            if sizes[i] >= min_size:
                min_size = sizes[i]
                # Mask of only the largest object
                mask_largest[output == i + 1] = 255
                image_origin[output == i + 1] = [0, 255, 0]
                (cX, cY) = centroids[i + 1]

        # If there are objects
        if nb_components > 0:
            # Draws cross at the center of the object
            cv2.line(image_origin, (int(cX)-10, int(cY)), (int(cX)+10, int(cY)), (0, 0, 255), 2)
            cv2.line(image_origin, (int(cX), int(cY)-10), (int(cX), int(cY)+10), (0, 0, 255), 2)

            # If it is a new line, paint a circle in the centroid of the object
            if flag_newline == 1:
                cv2.circle(image_sketch, (int(cX), int(cY)), 0, (0, 0, 255), 2)
                cX_past = cX
                cY_past = cY
                flag_newline = 0

            # If it is a continuation of a line, draw a line between the new centroid and the last centroid
            else:
                cv2.line(image_sketch, (int(cX_past), int(cY_past)), (int(cX), int(cY)), (0, 0, 255), 2)
                cX_past = cX
                cY_past = cY

        # If no objects are present, reset the flag for a new line
        else:
            flag_newline = 1

        # Image windows
        cv2.imshow('window_mask', mask)
        cv2.imshow('window_mask_largest', mask_largest)
        cv2.imshow('window_origin', image_origin)
        cv2.imshow(window_name, image_sketch)

        #Stop the program when 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == '__main__':
    main()

