import time
import argparse
import sys
import copy
from os.path import join
from collections import defaultdict

def partOne(data):
    grid = defaultdict(lambda: '.')
    xIndex = []
    
    #Make the list a dict, this isnt needed here, but I like to do this for some reason
    for line in range(len(data)):
        for elem in range(len(data[line])):
            grid[(line,elem)] = data[line][elem]
            if data[line][elem] == 'X':
                xIndex.append((line,elem))
    
    #For each X, check all around it for an XMAS in the 8 directions
    total = 0
    for start in xIndex:
        y, x = start
        UR = grid[start] + grid[(y-1, x+1)] + grid[(y-2, x+2)] + grid[(y-3, x+3)]
        U = grid[start] + grid[(y-1, x)] + grid[(y-2, x)] + grid[(y-3, x)]
        UL = grid[start] + grid[(y-1, x-1)] + grid[(y-2, x-2)] + grid[(y-3, x-3)]
        R = grid[start] + grid[(y, x+1)] + grid[(y, x+2)] + grid[(y, x+3)]
        L = grid[start] + grid[(y, x-1)] + grid[(y, x-2)] + grid[(y, x-3)]
        DR = grid[start] + grid[(y+1, x+1)] + grid[(y+2, x+2)] + grid[(y+3, x+3)]
        D = grid[start] + grid[(y+1, x)] + grid[(y+2, x)] + grid[(y+3, x)]
        DL = grid[start] + grid[(y+1, x-1)] + grid[(y+2, x-2)] + grid[(y+3, x-3)]
        temp = [UR, U, UL, R, L, DR, D, DL]
        total += sum([1 for x in temp if x  == 'XMAS'])
    return total

def partTwo(data):
    grid = defaultdict(lambda: '.')
    aIndex = []
    
    #Make the list a dict, this isnt needed here, but I like to do this for some reason
    for line in range(len(data)):
        for elem in range(len(data[line])):
            grid[(line,elem)] = data[line][elem]
            if data[line][elem] == 'A':
                aIndex.append((line,elem))
    
    #For each A, Check its corners, and see if opposite corners are M and S combined.
    total = 0
    for start in aIndex:
        y, x = start
        UR = grid[(y-1, x+1)]
        UL = grid[(y-1, x-1)]
        DR = grid[(y+1, x+1)]
        DL = grid[(y+1, x-1)]
        #UR and DL need to be either an M or S, and cant be equal
        if {DL, UR} == {"M", "S"} and {UL, DR} == {"M", "S"}:
            total += 1
    return total

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