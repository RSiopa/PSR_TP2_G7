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

    data = json.load(open(args['json']))
    dict_json = data['limits']
    print(dict_json)


if __name__ == '__main__':
    main()

