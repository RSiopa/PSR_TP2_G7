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
from color_segmenter import *

parser = argparse.ArgumentParser(description='Definition of test mode')     # arguments
parser.add_argument('-j', '--json', type=str, help='Full path to json file.\n ')
args = vars(parser.parse_args())


def main():

    with open('limits.json') as json_file:
        data = json.load(args['json'])
        for p in data['people']:
            print('Name: ' + p['name'])
            print('Website: ' + p['website'])
            print('From: ' + p['from'])
            print('')


if __name__ == '__main__':
    main()

