#!/usr/bin/python3.8
# --------------------------------------------------
# Python script for color adjustment and saving the values to a json file.
# Rafael Inacio Siopa.
# Frederico Ribeiro e Martins.
# Rodrigo Dinis Martins Ferreira.
# Bartosz Bartosik.
# PSR, November 2021.
# --------------------------------------------------
import argparse
import copy

from numpy import zeros

from color_segmenter import *

parser = argparse.ArgumentParser(description='Definition of test mode')     # arguments
parser.add_argument('-j', '--json', type=str, help='Full path to json file.\n ')
args = vars(parser.parse_args())


def main():

    # -----------------------------------------------------------
    # Initialization
    # -----------------------------------------------------------

    # Read dictionary in Json file
    data = json.load(open(args['json']))
    dict_json = data['limits']

    # Video capture setup
    window_name = 'window_sketch'
    cv2.namedWindow(window_name)
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FPS, 15)

    # White image aka Sketch created
    _, image = capture.read()
    h = len(image)
    w = len(image[0])
    image_sketch = zeros([h, w, 3])

    for y in range(h):
        for x in range(w):
            image_sketch[y, x] = [255, 255, 255]

    # -----------------------------------------------------------
    # Continuous Operation
    # -----------------------------------------------------------

    cv2.imshow(window_name, image_sketch)
    cv2.waitKey()

if __name__ == '__main__':
    main()

