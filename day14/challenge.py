import time
import argparse
import sys
import copy
from os.path import join

def partOne(data):
    bounds = (101,103)
    xsplit = (bounds[0]+1) / 2
    ysplit = (bounds[1]+1) / 2
    simTime = 100
    robots = []
    for line in data:
        first, second = line.strip().split(' ')
        origin = [int(x) for x in first[2:].split(',')]
        speed = [int(x) for x in second[2:].split(',')]
        robots.append([origin, speed])
    finalPositions = []
    for robot in robots:
        x = (robot[0][0] + robot[1][0] * simTime)%bounds[0]
        y = (robot[0][1] + robot[1][1] * simTime)%bounds[1]
        finalPositions.append((x+1,y+1))
    quads = [[],[],[],[]]
    for x,y in finalPositions:
        if x < xsplit and y < ysplit:
            quads[0].append((x,y))
        if x > xsplit and y < ysplit:
            quads[1].append((x,y))
        if x < xsplit and y > ysplit:
            quads[2].append((x,y))
        if x > xsplit and y > ysplit:
            quads[3].append((x,y))

    return(len(quads[0])*len(quads[1])*len(quads[2])*len(quads[3]))

def partTwo(data):
    bounds = (101,103)
    xsplit = (bounds[0]+1) / 2
    ysplit = (bounds[1]+1) / 2
    simTime = 100
    robots = []
    for line in data:
        first, second = line.strip().split(' ')
        origin = [int(x) for x in first[2:].split(',')]
        speed = [int(x) for x in second[2:].split(',')]
        robots.append([origin, speed])
    
    secs = 0
    for time in range(10000000):
        finalPositions = []
        for robot in robots:
            x = (robot[0][0] + robot[1][0] * time)%bounds[0]
            y = (robot[0][1] + robot[1][1] * time)%bounds[1]
            finalPositions.append((x+1,y+1))
        temp = set(finalPositions)
        if len(finalPositions) == len(temp): 
            secs = time
            break

    for y in range(bounds[1]):
        line = ""
        for x in range(bounds[0]):
            append = "X" if (x,y) in finalPositions else " "
            line = line + append
        print(line)
    return secs

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