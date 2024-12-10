import time
import argparse
import sys
import copy
from os.path import join
from collections import defaultdict
import sys

def getValidSteps(map, position):
    valid = []
    for x in range(-1,2):
        for y in range(-1,2):
            if abs(x+y) == 1:
                if map[(position[0] + x,position[1] + y)] - map[position] == 1:
                    valid.append((position[0] + x,position[1] + y))
    return valid

def walkTrail(map, position, curTotal):
    if map[position] == 9:
        return {position}
    total = []
    for step in getValidSteps(map, position):
        total+=(walkTrail(map, step, curTotal))
    return total


def partOne(data):
    map = defaultdict(lambda:-10, {(x,y) : int(data[y][x]) for y in range(len(data)) for x in range(len(data[y])) if data[y][x] != "\n"})
    trailHeads =[(x,y) for y in range(len(data)) for x in range(len(data[y])) if data[y][x] == "0"]
    
    trailHeadScores = {head: walkTrail(map, head, 0) for head in trailHeads}
    
    return (sum([len(set(trailHeadScores[x])) for x in trailHeadScores]))

def partTwo(data):
    map = defaultdict(lambda:-10, {(x,y) : int(data[y][x]) for y in range(len(data)) for x in range(len(data[y])) if data[y][x] != "\n"})
    trailHeads =[(x,y) for y in range(len(data)) for x in range(len(data[y])) if data[y][x] == "0"]
    
    trailHeadScores = {head: walkTrail(map, head, 0) for head in trailHeads}
    
    return (sum([len(trailHeadScores[x]) for x in trailHeadScores]))

def main(fileName):
    data = []
    with open(fileName, 'r') as file:
        data = file.readlines()

    start_time = time.time()
    
    print(partOne(data))
    print(partTwo(data))
    
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', help='use the test input or not', 
                        action='store_false', required=False)
    args = parser.parse_args()
    fileName =join(sys.path[0],( "input" if args.test else "TestInput"))
    main(fileName)