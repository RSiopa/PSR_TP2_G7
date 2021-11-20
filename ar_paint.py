#!/usr/bin/env python3
# --------------------------------------------------
# Python script with a variety of painting functions!
# Rafael Inacio Siopa.
# Rodrigo Dinis Martins Ferreira.
# Bartosz Bartosik.
# Frederico Ribeiro e Martins.
# PSR, November 2021.
# --------------------------------------------------
import argparse
import copy
from datetime import datetime
from functools import partial

from numpy import zeros
from color_segmenter import *

drawing = False
ix = -1
iy = -1

# Argument
parser = argparse.ArgumentParser()
parser.add_argument('-j', '--json', type=str, help='Full path to json file.\n ')
parser.add_argument('-usp', '--use_shake_prevention', action='store_true', help='When activated prevents random '
                                                                                'scribbles due to fast movement.\n ')
args = vars(parser.parse_args())

# Mouse function
def MouseCoord(event, x, y, flags, params, window_name, img, color, thickness):
    global drawing, ix, iy
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix = x
        iy = y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.line(img, (ix, iy), (x, y), color, thickness)
            ix = x
            iy = y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(img, (ix, iy), (x, y), color, thickness)


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

    # White image aka image_sketch created
    _, image = capture.read()
    h = len(image)
    w = len(image[0])
    image_sketch = zeros([h, w, 3])
    image_sketch2 = copy.copy(image)

    for y in range(h):
        for x in range(w):
            image_sketch[y, x] = [255, 255, 255]
            image_sketch2[y, x] = 255

    # Mins and maxs acquired from dictionary in Json file
    mins = np.array([limits['B']['min'], limits['G']['min'], limits['R']['min']])
    maxs = np.array([limits['B']['max'], limits['G']['max'], limits['R']['max']])

    # Variable for when cv2.connectedComponentsWithStats is used (can be 8 too)
    connectivity = 4

    # Flag for the program to know that the user just started to draw a new line (lines can be disconnected)
    flag_newline = 1

    print('\nPress r to change to red color.'
          '\nPress g to change to green color.'
          '\nPress b to change to blue color.'
          '\nPress + to increase the thickness of the pencil'
          '\nPress - to decrease the thickness of the pencil'
          '\nPress m to use the mouse as the pencil.'
          '\nPress v to change the white board to the video stream.'
          '\nPress c to clear the sketch'
          '\nPress w to save the sketch'
          '\nInitializing with red color as default.')

    color = (0, 0, 255)       #Default color for the sketch
    thickness = 2             #Default thickness of the pencil
    cX_past = 0
    cY_past = 0
    cX = 0
    cY = 0

    flag_mouse = 0

    flag_video = 0

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

            if flag_mouse == 0:
                # If it is a new line, paint a circle in the centroid of the object
                if flag_newline == 1 and args['use_shake_prevention']:
                    cv2.circle(image_sketch, (int(cX), int(cY)), 0, color, thickness)
                    cv2.circle(image_sketch2, (int(cX), int(cY)), 0, color, thickness)
                    cX_past = cX
                    cY_past = cY
                    flag_newline = 0

                # If it is a continuation of a line, draw a line between the new centroid and the last centroid
                else:
                    cv2.line(image_sketch, (int(cX_past), int(cY_past)), (int(cX), int(cY)), color, thickness)
                    cv2.line(image_sketch2, (int(cX_past), int(cY_past)), (int(cX), int(cY)), color, thickness)
                    cX_past = cX
                    cY_past = cY


        # If no objects are present, reset the flag for a new line
        else:
            flag_newline = 1

        # Image windows
        cv2.imshow('window_mask', mask)
        cv2.imshow('window_mask_largest', mask_largest)
        cv2.imshow('window_origin', image_origin)

        if flag_video == 0:
            cv2.imshow(window_name, image_sketch)
        else:
            # image_sketch2[np.where(image_sketch2 == 255)] = image[np.where(image_sketch2 == 255)]
            cv2.imshow(window_name, image_sketch2)

        # Changes the mouse color and thickness
        MouseCoord_paint = partial(MouseCoord, window_name=window_name, img=image_sketch, color=color,
                                   thickness=thickness)
        # Changes modes if flag_mouse changes
        if flag_mouse == 1:
            cv2.setMouseCallback(window_name, MouseCoord_paint)
        else:
            cv2.setMouseCallback(window_name, lambda *args: None)

        key = cv2.waitKey(20)

        if key == ord('q'):                    # Stops the program when 'q' is pressed
            break
        if key == ord('r'):                    # Changes the pencil color to red when 'r' is pressed
            color = (0, 0, 255)
        if key == ord('g'):                    # Changes the pencil color to green when 'g' is pressed
            color = (0, 255, 0)
        if key == ord('b'):                    # Changes the pencil color to blue when 'b' is pressed
            color = (255, 0, 0)
        if key == ord('+'):                    # Increases the pencil thickness when '+' is pressed
            thickness += 1
        if key == ord('-') and thickness > 1:  # Decreases the pencil thickness when '-' is pressed
            thickness -= 1
        if key == ord('m'):                    # Switches between using the mouse or not to paint when 'm' is pressed
            flag_mouse = not flag_mouse
        if key == ord('v'):                    # Switches between using the blank image and the video stream to paint
                                               # when 'm' is pressed
            flag_video = not flag_video
        if key == ord('c'):                    # Clears the sketch when 'c' is pressed
            for y in range(h):
                for x in range(w):
                    image_sketch[y, x] = [255, 255, 255]
                    #image_sketch_over = copy.copy(image)
        if key == ord('w'):                    # Saves the sketch when 'w' is pressed
            filename = datetime.now().strftime('drawing_'+"%a_%b_%d_%H:%M:%S_%Y"+'.jpg')
            cv2.imwrite(filename, image_sketch)
            print(filename + ' saved.')


if __name__ == '__main__':
    main()

