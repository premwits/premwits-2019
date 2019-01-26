# This file is intended to be used as a game simulator
# The simulation could be done by running `python3 main.py`
# usage: main.py [-h] [-n [NUMBER]] [-t [TIME]] [-m [MAX_HP]]
# Simulate PreMWIT 2019 Game.
# optional arguments:
#   -h, --help            show this help message and exit
#   -n [NUMBER], --number [NUMBER]
#                         number of participants
#   -t [TIME], --time [TIME]
#                         total time used (in seconds)
#   -m [MAX_HP], --max-hp [MAX_HP]
#                         maximum hitpoint
#   -r [DECREMENT_RATE], --decrement-rate [DECREMENT_RATE]
#                         decrement rate (hp/sec)
import argparse
import random

def student_number(x):
    x = int(x)
    if x <= 0:
        raise argparse.ArgumentError('Number of students must be positive integer')
    return x

def time(x):
    x = int(x)
    if x < 580:
        raise argparse.ArgumentError('Time must be more than 580')
    return x

def max_hp(x):
    x = int(x)
    if x <= 0:
        raise argparse.ArgumentError('Hitpoint must be positive integer')
    return x

parser = argparse.ArgumentParser(description='Simulate PreMWIT 2019 Game.')
parser.add_argument('-n', '--number', type=int, nargs='?', help='number of participants (positive integer)')
parser.add_argument('-t', '--time', type=int, nargs='?', help='total time used (in seconds)')
parser.add_argument('-m', '--max-hp', type=int, nargs='?', help='maximum hitpoint')
parser.add_argument('-r', '--decrement-rate', type=int, nargs='?', help='decrement rate (hp/sec)')
args = parser.parse_args()
n = args.number if args.number != None else 200
t = args.time if args.time != None else 360000
m = args.max_hp if args.max_hp != None else 1000000000
r = args.decrement_rate if args.decrement_rate != None else t//100
time_step = 1 # seconds

# For cards:
# 1 stands for group
# 2 stands for fulfill
# 3 stands for recreation
# 4 stands for activity
# 5 stands for carry
# 6 stands for pr
# 7 stands for disguise
# 8 stands for art
# 9 stands for none
staff_cards = [0,80,40,40,60,50,40,40,4]
head_cards  = [0,5,5,5,5,5,5,5,5]
prop_cards  = [0,25,25,25,25,25,25,25,15]
print('staff_cards',sum(staff_cards))
print('head_cards',sum(head_cards))
print('prop_cards',sum(prop_cards))
card_dist = random.sample(range(1,t+1),sum(staff_cards) + sum(head_cards) + sum(prop_cards))

class Card:
    def __init__(self, ctype, subtype, time=None):
        self.type = ctype # staff, head, prop
        self.subtype = subtype # 1 to 8
        self.time = time # in seconds since start

    def __lt__(self, other):
        return self.time < other.time

    def __translate__(subtype):
        if subtype == 1:
            return 'group'
        elif subtype == 2:
            return 'fulfill'
        elif subtype == 3:
            return 'recreation'
        elif subtype == 4:
            return 'activity'
        elif subtype == 5:
            return 'carry'
        elif subtype == 6:
            return 'pr'
        elif subtype == 7:
            return 'disguise'
        elif subtype == 8:
            return 'art'
        elif subtype == 9:
            return 'none'
        else:
            return 'error'

    def __str__(self):
        return self.type + '-' + Card.__translate__(self.subtype) + ',' + str(self.time)

    def __eq__(self, other):
        return self.type == other.type and self.subtype == other.subtype and self.time == other.time
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash(self.type) + 2 * hash(self.subtype) + 3 * hash(self.time)

cards = []
index = 0
dtime = {}
for i in range(1,9):
    for j in range(staff_cards[i]):
        c = Card('staff',i,card_dist[index + j])
        dtime[card_dist[index + j]] = c
        cards.append(c)
    index += staff_cards[i]
    for j in range(head_cards[i]):
        c = Card('head',i,card_dist[index + j])
        dtime[card_dist[index + j]] = c
        cards.append(c)
    index += head_cards[i]
    for j in range(prop_cards[i]):
        c = Card('prop',i,card_dist[index + j])
        dtime[card_dist[index + j]] = c
        cards.append(c)
    index += prop_cards[i]

hp = 0
for step in range(1,t+1):
    hp -= r
    if hp < 0:
        hp = 0
    if step in dtime:
        cur = dtime[step]
        
