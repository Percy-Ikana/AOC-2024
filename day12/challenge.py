import time
import argparse
import sys
import copy
from os.path import join
from collections import defaultdict
from itertools import takewhile

def buildRegions(data):
    regions = []#defaultdict(lambda:set())
    #This is to exclude things that already have a home
    containedSquares = set()
    for square in data:
        if square in containedSquares: continue # already know where it belongs, skip it.
        region = {square}
        toCheck = {(square[0]+x,square[1]+y)  for x in [-1,0,1] for y in [-1,0,1] if (square[0]+x,square[1]+y) in data and abs(x)+abs(y) == 1 and data[(square[0]+x,square[1]+y)] == data[square] and (square[0]+x,square[1]+y) not in region}
        while len(toCheck) != 0:
            cur = toCheck.pop()
            region.add(cur)
            toCheck.update({(cur[0]+x,cur[1]+y)  for x in [-1,0,1] for y in [-1,0,1] if (cur[0]+x,cur[1]+y) in data and abs(x)+abs(y) == 1 and data[(cur[0]+x,cur[1]+y)] == data[cur] and (cur[0]+x,cur[1]+y) not in region})
        containedSquares.update(region)
        regions.append(region)
    return regions

def getTouchingInDir(dir, origin, data):
    edgeverts = []
    offset = (origin[0]+dir[0], origin[1]+dir[1])
    cont = offset in data
    
    while cont:
        edgeverts.append(offset)
        offset = (offset[0]+dir[0], offset[1]+dir[1])
        cont = offset in data
    
    if dir[0] < 0 or dir[1] < 0:
        edgeverts.reverse()
    
    return edgeverts

def partOne(data):
    data = {(x,y):data[y][x] for y in range(len(data)) for x in range(len(data[y].strip()))}
    #This might become a list of lists
 
    regions = buildRegions(data)
    
    data = defaultdict(lambda: -1, data)
    #well we now have the regions, so for each region we find the area (len) and how many "exposed" edges there are
    costs = []
    for region in regions:
        area = len(region)
        edges = []
        for square in region:
            edges+=[(square[0]+x,square[1]+y)  for x in [-1,0,1] for y in [-1,0,1] if abs(x)+abs(y) == 1 and data[(square[0]+x,square[1]+y)] != data[square]]
        perim = len(edges)
        cost = perim*area
        costs.append(cost)
    
    return sum(costs)

def partTwo(data):
    data = {(x,y):data[y][x] for y in range(len(data)) for x in range(len(data[y].strip()))}
    #This might become a list of lists
 
    regions = buildRegions(data)
    
    data = defaultdict(lambda: -1, data)
    
    #We just need to count corners but Im an idiot i guess.
    
    
    costs = []
    for region in regions:
        area = len(region)
        edges = []
        corners = 0
        
        for square in data:
           
            if square in region: continue
        
            touching = [(x,y)  for x in [-1, 0, 1] for y in [-1, 0 ,1] if (square[0]+x,square[1]+y) in region]

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