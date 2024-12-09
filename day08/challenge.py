import time
import argparse
import sys
import copy
from os.path import join
from collections import defaultdict
from itertools import combinations

def addTuple(tuple1, tuple2, mod = 1):
    return (tuple1[0] + (tuple2[0]*mod), tuple1[1] + (tuple2[1]*mod))

def partOne(data):
    bounds = (range(len(data[0].strip())), range(len(data)))
    ants = defaultdict(lambda: [])
    [ants[data[y][x]].append((x,y)) for y in range(len(data)) for x in range(len(data[y].strip())) if data[y][x] != '.']
    #Okay so now for each key, we make pairs of them all?

    antinodes = set()
    for key in ants.keys():
        if len(ants[key]) > 1:
            for pair in combinations(ants[key], 2):
                # find the taxicab distance
                dist = (pair[0][0] - pair[1][0], pair[0][1] - pair[1][1])
                nodes = {addTuple(pair[0], dist, 1), addTuple(pair[0], dist, -1), addTuple(pair[1], dist, 1), addTuple(pair[1], dist, -1)} - {pair[0], pair[1]}
                for node in copy.deepcopy(nodes):
                    if node[0] not in bounds[0] or node[1] not in bounds[1]:
                        nodes.remove(node)
                antinodes = antinodes.union(nodes)
    return len(antinodes)

def partTwo(data):
    bounds = (range(len(data[0].strip())), range(len(data)))
    ants = defaultdict(lambda: [])
    [ants[data[y][x]].append((x,y)) for y in range(len(data)) for x in range(len(data[y].strip())) if data[y][x] != '.']
    #Okay so now for each key, we make pairs of them all?

    antinodes = set()
    for key in ants.keys():
        if len(ants[key]) > 1:
            for pair in combinations(ants[key], 2):
                # find the taxicab distance
                dist = (pair[0][0] - pair[1][0], pair[0][1] - pair[1][1])
                #add all negative antinodes
                mul = 1
                nodes = {pair[0], pair[1]}
                while True:
                    Antinode = addTuple(pair[0], dist, -1*mul)
                    if Antinode[0] in bounds[0] and Antinode[1] in bounds[1]:
                        mul +=1
                        nodes.add(Antinode)
                    else:
                        break
                #all positive
                mul = 1
                while True:
                    Antinode = addTuple(pair[0], dist, 1*mul)
                    if Antinode[0] in bounds[0] and Antinode[1] in bounds[1]:
                        mul +=1
                        nodes.add(Antinode)
                    else:
                        break
                
                for node in copy.deepcopy(nodes):
                    if node[0] not in bounds[0] or node[1] not in bounds[1]:
                        nodes.remove(node)
                antinodes = antinodes.union(nodes)
    return len(antinodes)

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