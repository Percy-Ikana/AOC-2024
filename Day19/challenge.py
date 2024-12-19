import time
import argparse
import sys
import copy
from os.path import join

towels = []
patterns = []
seen = {}
valid = {}

def findMatches(pattern, index):
    if (pattern, index) in seen:
        return seen[(pattern, index)]
    if index == len(pattern):
        seen[(pattern, index)] = 1 
        return 1
    matches = 0
    for towel in towels:
        towelSize = len(towel)
        if pattern[index:index+towelSize] == towel:
            matches += findMatches(pattern, index+towelSize)
    seen[(pattern, index)] = matches
    return matches

def partOne(data):
    global towels, patterns, valid
    towels = [x.strip() for x in data[0].strip().split(",")]
    patterns = [x.strip() for x in data[2:]]
    for pattern in patterns:
        valid[pattern] = findMatches(pattern, 0)
    return len([x for x in valid if valid[x] > 0]) 

def partTwo(data):
    return sum(valid.values()) 

def main(fileName):
    data = []
    with open(fileName, 'r') as file:
        data = file.readlines()

    start_time = time.time()
    
    print(partOne(data))
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    print(partTwo(data))
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', help='use the test input or not', 
                        action='store_false', required=False)
    args = parser.parse_args()
    fileName =join(sys.path[0],( "input" if args.test else "TestInput"))
    main(fileName)