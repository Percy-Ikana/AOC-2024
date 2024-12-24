import time
import argparse
import sys
import copy
from os.path import join
from collections import defaultdict
import itertools

def partOne(data):
    connections = defaultdict(lambda:set())
    for connection in data:
        comp1, comp2 = connection.strip().split("-")
        connections[comp1].add(comp2)
        connections[comp2].add(comp1)

    tris = set()
    for computer in connections.keys():
        for comp1, comp2 in itertools.combinations(connections[computer], 2):
            if comp2 in connections[comp1]:
                tris.add(tuple(sorted([computer, comp1, comp2])))
    
    final = set()
    for comp1, comp2, comp3 in tris:
        if comp1[0] == "t" or comp2[0] == "t" or comp3[0] == "t":
            final.add((comp1, comp2, comp3))
            
    return len(final)


def partTwo(data):
    
    connections = defaultdict(lambda:[])
    for connection in data:
        comp1, comp2 = connection.strip().split("-")
        connections[comp1].append(comp2)
        connections[comp2].append(comp1)
    
    largest = defaultdict(lambda:set())
    try:
        for i in range(14,2, -1):
            pass
            for computer in connections.keys():
                for comps in itertools.combinations(connections[computer], i):
                    isSet = all([all([x in connections[y] for y in comps if x!=y]) for x in comps])
                    if isSet:
                        #im assuming there is only one largest graph, so once we find it, leave
                        largest[i].add(','.join(sorted(list(comps) + [computer])))
                        raise Exception
    except Exception:
        pass

    counts = defaultdict(lambda: 0)
    for connList in connections:
        counts[','.join(sorted(list(connections[connList])))] += 1

    return largest[max(largest.keys())]

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