# This file is intended to be used as a game simulator
# The simulation could be done by running `python3 main.py`

import argparse

parser = argparse.ArgumentParser(description='Simulate PreMWIT 2019 Game.')
parser.add_argument('-n', '--number', type=int, nargs='?', help='number of participants')
parser.add_argument('-t', '--time', type=int, nargs='?', help='total time used (in seconds)')
parser.add_argument('-m', '--max-hp', type=int, nargs='?', help='maximum hitpoint')
args = parser.parse_args()
print(args)