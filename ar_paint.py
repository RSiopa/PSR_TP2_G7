#!/usr/bin/env python3
# --------------------------------------------------
# Python script with a variety of painting functionalities!
# Rafael Inacio Siopa.
# Rodrigo Dinis Martins Ferreira.
# Bartosz Bartosik.
# PSR, November 2021.
# --------------------------------------------------
import argparse
import copy
import math
from datetime import datetime
from functools import partial
from color_segmenter import *
from colorama import Fore, Style

drawing = False
ix = -1
iy = -1

# Argparse argument
parser = argparse.ArgumentParser()
parser.add_argument('-j', '--json', required=True, type=str, help='Full path to json file.\n ')
parser.add_argument('-usp', '--use_shake_prevention', action='store_true', help='When activated prevents old ends of a'
                                                                                ' line from connecting to new lines.\n')
parser.add_argument('-i', '--image_to_paint', type=int, help='Number of the picture you want to paint (1, 2 or 3).\n ')
args = vars(parser.parse_args())


# Mouse function (for 2 separate images)
def MouseCoord(event, x, y, flags, params, flag_video, window_name, img, img2, color, thickness, drawing_type, image_video):
    global drawing, ix, iy, x_, y_

    # Drawing rectangles
    if drawing_type == 'square':
        # When left mouse button is pressed
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y
            x_, y_ = x, y


        # When mouse is moving
        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            if flag_video is True:
                copy_img = image_video.copy()
            else:
                copy_img = img.copy()

            x_, y_ = x, y

            cv2.rectangle(copy_img, (ix, iy), (x_, y_), color, thickness)

            cv2.imshow(window_name, copy_img)

        # When releasing left mouse button
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            cv2.rectangle(img, (ix, iy), (x, y), color, thickness)
            cv2.rectangle(img2, (ix, iy), (x, y), color, thickness)

    # Drawing circles
    elif drawing_type == 'circle':
        # When left mouse button is pressed
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y
            x_, y_ = x, y

        # When mouse is moving
        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            if flag_video is True:
                copy_image = image_video.copy()
            else:
                copy_image = img.copy()

            x_, y_ = x, y

            cv2.circle(copy_image, (ix, iy), round(math.sqrt((x_-ix)**2 + (y_-iy)**2)), color, thickness)

            cv2.imshow(window_name, copy_image)

        # When releasing left mouse button
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            cv2.circle(img, (ix, iy), round(math.sqrt((x-ix)**2 + (y-iy)**2)), color, thickness)
            cv2.circle(img2, (ix, iy), round(math.sqrt((x-ix)**2 + (y-iy)**2)), color, thickness)

    # Default drawing
    else:
        # When left mouse button is pressed
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix = x
            iy = y

        # When mouse is moving
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing is True:
                cv2.line(img, (ix, iy), (x, y), color, thickness)
                cv2.line(img2, (ix, iy), (x, y), color, thickness)
                ix = x
                iy = y

        # When releasing left mouse button
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            cv2.line(img, (ix, iy), (x, y), color, thickness)
            cv2.line(img2, (ix, iy), (x, y), color, thickness)


def main():

    # -----------------------------------------------------------
    # Initialization
    # -----------------------------------------------------------

    print("\nWelcome to our Augmented Reality Paint program. \n\nContributors: "
          "\n- Rafael Inacio Siopa \n- Rodrigo Dinis Martins Ferreira "
          " \n- Bartosz Bartosik \n\nPSR, University of Aveiro, "
          "November 2021.\n")

    # Read dictionary from json file and put it in 'limits' variable
    data = json.load(open(args['json']))
    limits = data['limits']

    # Video capture setup
    window_name = 'window_sketch'
    cv2.namedWindow(window_name)
    capture = cv2.VideoCapture(0)
    _, image = capture.read()

    # White images created
    h = len(image)
    w = len(image[0])
    image_sketch = np.ones([h, w, 3], dtype=np.uint8) * 255
    image_sketch2 = np.ones([h, w, 3], dtype=np.uint8) * 255

    # Dictionary for the pictures that the user will choose to paint
    picture_dict = {1: 'cupcake.png', 2: 'ball.png', 3: 'butterfly.png'}

    # Dictionary for the pictures perfectly painted
    perfect_dict = {1: 'cupcake_perfect.png', 2: 'ball_perfect.png', 3: 'butterfly_perfect.png'}

    # If user wants to paint an image, image_sketch is now the image to paint
    if args['image_to_paint'] is not None:
        # Put the image chosen in a variable, then resize it to the size of the webcam video and make a copy
        # to maintain the original
        image_file = picture_dict[args['image_to_paint']]
        num_paint = cv2.imread(image_file, cv2.IMREAD_COLOR)
        resized = cv2.resize(num_paint, (w, h), interpolation=cv2.INTER_AREA)
        image_sketch = copy.copy(resized)

        # Put the perfectly painted image in a variable and resize it.
        perfect_image = cv2.imread(perfect_dict[args['image_to_paint']], cv2.IMREAD_COLOR)
        perfect_resized = cv2.resize(perfect_image, (w, h), interpolation=cv2.INTER_AREA)

    # Mins and maxs acquired from dictionary in Json file in limits variable
    mins = np.array([limits['B']['min'], limits['G']['min'], limits['R']['min']])
    maxs = np.array([limits['B']['max'], limits['G']['max'], limits['R']['max']])

    # Variable for when cv2.connectedComponentsWithStats is used (can be 8 too)
    connectivity = 4

    # Flag for the program to know that the user just started to draw a new line (lines can be disconnected)
    flag_newline = 1

    print('\nPress ' + Fore.GREEN + 'r' + Style.RESET_ALL + ' to change to ' + Fore.YELLOW + 'red color' + Style.RESET_ALL + '.'
          '\nPress ' + Fore.GREEN + 'g' + Style.RESET_ALL + ' to change to ' + Fore.YELLOW + 'green color' + Style.RESET_ALL + '.'
          '\nPress ' + Fore.GREEN + 'b' + Style.RESET_ALL + ' to change to ' + Fore.YELLOW + 'blue color' + Style.RESET_ALL + '.'
          '\nPress ' + Fore.GREEN + 'y' + Style.RESET_ALL + ' to change to ' + Fore.YELLOW + 'yellow color' + Style.RESET_ALL + '.'
          '\nPress ' + Fore.GREEN + 'p' + Style.RESET_ALL + ' to change to ' + Fore.YELLOW + 'orange color' + Style.RESET_ALL + '.'
          '\nPress ' + Fore.GREEN + 'k' + Style.RESET_ALL + ' to change to ' + Fore.YELLOW + 'black color' + Style.RESET_ALL + '.'
          '\nPress ' + Fore.GREEN + '+' + Style.RESET_ALL + ' to ' + Fore.YELLOW + 'increase the thickness' + Style.RESET_ALL + ' of the pencil'
          '\nPress ' + Fore.GREEN + '-' + Style.RESET_ALL + ' to ' + Fore.YELLOW + 'decrease the thickness' + Style.RESET_ALL + ' of the pencil'
          '\nPress ' + Fore.GREEN + 'm' + Style.RESET_ALL + ' to use the ' + Fore.YELLOW + 'mouse' + Style.RESET_ALL + ' as the pencil.'
          '\nPress ' + Fore.GREEN + 'v' + Style.RESET_ALL + ' to change the white board to the ' + Fore.YELLOW + 'video stream' + Style.RESET_ALL + '.'
          '\nPress ' + Fore.GREEN + 's' + Style.RESET_ALL + ' to draw ' + Fore.YELLOW + 'squares' + Style.RESET_ALL + '.'
          '\nPress ' + Fore.GREEN + 'o' + Style.RESET_ALL + ' to draw ' + Fore.YELLOW + 'circles' + Style.RESET_ALL + '.'
          '\nPress ' + Fore.GREEN + 'c' + Style.RESET_ALL + ' to ' + Fore.YELLOW + 'clear' + Style.RESET_ALL + ' the sketch'
          '\nPress ' + Fore.GREEN + 'w' + Style.RESET_ALL + ' to ' + Fore.YELLOW + 'save' + Style.RESET_ALL + ' the sketch'
          '\nInitializing with color ' + Fore.RED + 'red' + Style.RESET_ALL + ' as default.')

    color = (0, 0, 255)                 # Default color for the sketch
    thickness = 2                       # Default thickness of the pencil

    # Used to save the x and y coordinates of the past point of the pencil
    cX_past = 0
    cY_past = 0

    # Used to save the x and y coordinates of the point of the pencil
    cX = 0
    cY = 0

    # Variable used for the program to know if the mouse is drawing
    flag_mouse = 0

    # Detect type of drawing mode
    drawing_type = 'default'
    flag_square = False
    flag_circle = False
    flag_figure_drawing_in_progress = False

    # When flag_video is 1, the program replaces the white board by the realtime webcam video
    flag_video = 0

    # When evaluation is 1, the program does the evaluation of the drawing (Advanced functionality 5)
    evaluation = 0

    # -----------------------------------------------------------
    # Continuous Operation
    # -----------------------------------------------------------

    while True:

        # Save the key pressed
        key = cv2.waitKey(20)

        _, image = capture.read()
        image_origin = copy.copy(image)
        # Mask gotten from mins and maxs
        mask = cv2.inRange(image_origin, mins, maxs)
        # Initialization of mask for only the largest object (in case the program detects no items at the start)
        mask_largest = np.zeros(mask.shape)

        # Gets number of components, stats and their centroids
        nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity, cv2.CV_32S)
        sizes = stats[1:, -1]
        nb_components = nb_components - 1
        min_size = 0
        for i in range(0, nb_components):
            # Goes through all the objects but only paints and gets centroid of the largest one
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

                else:
                    # If current drawing mode is set to Square
                    if drawing_type == 'square':
                        current_sketch = copy.deepcopy(image_sketch)
                        current_sketch2 = copy.deepcopy(image_sketch2)

                        flag_figure_drawing_in_progress = True
                        cv2.rectangle(current_sketch, (int(cX_past), int(cY_past)), (int(cX), int(cY)), color,
                                      thickness)
                        cv2.rectangle(current_sketch2, (int(cX_past), int(cY_past)), (int(cX), int(cY)), color,
                                      thickness)

                        if key == ord('s'):
                            cv2.rectangle(image_sketch, (int(cX_past), int(cY_past)), (int(cX), int(cY)), color,
                                          thickness)
                            cv2.rectangle(image_sketch2, (int(cX_past), int(cY_past)), (int(cX), int(cY)), color,
                                          thickness)
                            cX_past = cX
                            cY_past = cY
                            flag_figure_drawing_in_progress = False

                    # If current drawing mode is set to Circle
                    elif drawing_type == 'circle':
                        current_sketch = copy.deepcopy(image_sketch)
                        current_sketch2 = copy.deepcopy(image_sketch2)

                        flag_figure_drawing_in_progress = True
                        cv2.circle(current_sketch, (int(cX_past), int(cY_past)),
                                   round(math.sqrt((int(cX) - int(cX_past)) ** 2 + (int(cY) - int(cY_past)) ** 2)),
                                   color,
                                   thickness)
                        cv2.circle(current_sketch2, (int(cX_past), int(cY_past)),
                                   round(math.sqrt((int(cX) - int(cX_past)) ** 2 + (int(cY) - int(cY_past)) ** 2)),
                                   color,
                                   thickness)

                        if key == ord('o'):
                            cv2.circle(image_sketch, (int(cX_past), int(cY_past)), round(
                                math.sqrt((int(cX) - int(cX_past)) ** 2 + (int(cY) - int(cY_past)) ** 2)), color,
                                       thickness)
                            cv2.circle(image_sketch2, (int(cX_past), int(cY_past)), round(
                                math.sqrt((int(cX) - int(cX_past)) ** 2 + (int(cY) - int(cY_past)) ** 2)), color,
                                       thickness)
                            cX_past = cX
                            cY_past = cY
                            flag_figure_drawing_in_progress = False

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

        # Changes white board to video stream
        if flag_video == 0:
            # Show main image when rectangle/circle is not being drawn
            if not flag_figure_drawing_in_progress:
                cv2.imshow(window_name, image_sketch)
            # Else show image with rectangle/circle that is being drawn
            else:
                cv2.imshow(window_name, current_sketch)
            image_over_sketch = copy.copy(image_sketch)
        else:
            # Copy main image when rectangle/circle is not being drawn
            if not flag_figure_drawing_in_progress:
                image_over_sketch = copy.copy(image_sketch2)
                image_over_sketch[np.where(image_sketch2 == 255)] = image[np.where(image_sketch2 == 255)].copy()
            # Else copy image with rectangle/circle that is being drawn
            else:
                image_over_sketch = copy.copy(current_sketch2)
                image_over_sketch[np.where(current_sketch2 == 255)] = image[np.where(current_sketch2 == 255)].copy()
            cv2.imshow(window_name, image_over_sketch)

        params = [window_name, image_sketch, image_sketch2, color, thickness, drawing_type, flag_video, image_over_sketch]
        # Changes the mouse color, thickness, drawing type, etc.
        MouseCoord_paint = partial(MouseCoord, window_name=params[0], img=params[1], img2=params[2], color=params[3],
                                   thickness=params[4], drawing_type=params[5], flag_video=params[6], image_video=params[7])
        # Changes modes if flag_mouse changes
        if flag_mouse == 1:
            cv2.setMouseCallback(window_name, MouseCoord_paint)
        else:
            cv2.setMouseCallback(window_name, lambda *args: None)

        # Evaluates the drawing abilities of the user
        if evaluation == 1:
            cv2.imshow('Perfect painted', perfect_resized)
            print('Beginning evaluation...')
            total = h*w
            nottopaint = 0
            allEqual = 0
            for i in range(h):
                for j in range(w):
                    # Compare the perfect image and the original one to count the pixels that are not to paint
                    if np.all(perfect_resized[i, j] == resized[i, j]):
                        nottopaint += 1
            topaint = total - nottopaint
            for i in range(h):
                for j in range(w):
                    if np.all(perfect_resized[i, j] == image_sketch[i, j]):
                        allEqual += 1
            right = allEqual - nottopaint
            accuracy = right/topaint
            if accuracy < 0:
                accuracy = 0
            if accuracy > 0.9:
                print('You are an artist. It is perfect!')
                print('Accuracy=' + Fore.GREEN, round(accuracy * 100, 2), '%' + Style.RESET_ALL)
            elif accuracy == 0:
                print('What are you waiting for? Start drawing!')
                print('Accuracy=' + Fore.RED, round(accuracy * 100, 2), '%' + Style.RESET_ALL)
            elif accuracy < 0.5:
                print('Keep practicing. One day you will (probably) get it perfect.')
                print('Accuracy=' + Fore.MAGENTA, round(accuracy * 100, 2), '%' + Style.RESET_ALL)
            elif accuracy > 0.5:
                print('Well done. A little bit of practice and you will be the next Van Gogh!')
                print('Accuracy=' + Fore.YELLOW, round(accuracy * 100, 2), '%' + Style.RESET_ALL)
            evaluation = not evaluation

        if key == ord('q'):                    # Stops the program when 'q' is pressed
            break
        if key == ord('r'):                    # Changes the pencil color to red when 'r' is pressed
            color = (0, 0, 255)
        if key == ord('g'):                    # Changes the pencil color to green when 'g' is pressed
            color = (0, 255, 0)
        if key == ord('b'):                    # Changes the pencil color to blue when 'b' is pressed
            color = (255, 0, 0)
        if key == ord('y'):                    # Changes the pencil color to yellow when 'y' is pressed
            color = (0, 255, 255)
        if key == ord('p'):                    # Changes the pencil color to orange when 'p' is pressed
            color = (0, 165, 255)
        if key == ord('k'):                    # Changes the pencil color to black when 'k' is pressed
            color = (0, 0, 0)
        if key == ord('+'):                    # Increases the pencil thickness when '+' is pressed
            thickness += 1
        if key == ord('-') and thickness > 1:  # Decreases the pencil thickness when '-' is pressed
            thickness -= 1
        if key == ord('m'):                    # Switches between using the mouse or not to paint when 'm' is pressed
            flag_mouse = not flag_mouse
        if key == ord('v'):                    # Switches between using the blank image and the video stream to paint
            flag_video = not flag_video        # when 'v' is pressed
        if key == ord('c'):                    # Clears the sketch when 'c' is pressed
            image_sketch2 = np.ones([h, w, 3], dtype=np.uint8) * 255
            if args['image_to_paint'] is not None:
                image_sketch = copy.copy(resized)
            else:
                image_sketch = np.ones([h, w, 3], dtype=np.uint8) * 255
        if key == ord('w'):                    # Saves the sketch when 'w' is pressed
            filename = datetime.now().strftime('drawing_'+"%a_%b_%d_%H:%M:%S_%Y"+'.png')
            if flag_video is True:
                cv2.imwrite(filename, image_over_sketch)
            else:
                cv2.imwrite(filename, image_sketch)
            print(filename + ' saved.')
        if key == ord('e') and args['image_to_paint'] is not None:
            evaluation = not evaluation
        if key == ord('s') and flag_circle is False:        # Detect if 's' is pressed and toggle it
            flag_square = not flag_square
            if flag_square:
                drawing_type = 'square'
                print("You are now in square draw mode.")
            else:
                drawing_type = 'default'
                print("You switched to default draw mode.")
        elif key == ord('o') and flag_square is False:      # Detect if 'o' is pressed and toggle it
            flag_circle = not flag_circle
            if flag_circle:
                drawing_type = 'circle'
                print("You are now in circle draw mode.")
            else:
                drawing_type = 'default'
                print("You switched to default draw mode.")


if __name__ == '__main__':
    main()
