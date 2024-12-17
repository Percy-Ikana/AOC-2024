import time
import argparse
import sys
import copy
from os.path import join
from collections import defaultdict

import sys
sys.setrecursionlimit(99999)

turns = {
    (-1, 0): [(0,-1),(0,1)],
    (1, 0): [(0,-1),(0,1)],
    (0, -1): [(-1,0),(1,0)],
    (0, 1): [(-1,0),(1,0)]
}

paths = []
visited = defaultdict(int)

def addTuple(tupe1, tupe2):
    return (tupe1[0] + tupe2[0], tupe1[1] + tupe2[1])

def step(pos, seen, facing, cost, path, grid):
    global visited
    visited[pos]+=1
    
    if cost < seen[pos]:
        seen[pos] = cost
    
    if grid[pos] == "E":
        return path,"E" , cost
    
    options = []
    
    if grid[addTuple(pos, facing)] != "#" and seen[addTuple(pos, facing)] >= (cost + 1):
        options.append(step(addTuple(pos, facing), seen, facing, cost+1,path, grid))
        
    if grid[addTuple(pos, turns[facing][0])] != "#" and seen[addTuple(pos, turns[facing][0])] >= (cost + 1001):
        options.append(step(addTuple(pos, turns[facing][0]), seen, turns[facing][0], cost+1001, path, grid))
        
    if grid[addTuple(pos, turns[facing][1])] != "#" and seen[addTuple(pos, turns[facing][1])] >= (cost + 1001):
        options.append(step(addTuple(pos, turns[facing][1]), seen, turns[facing][1], cost+1001, path, grid))
        
    lowestCost = (path, "NE" , 1e20)
    for option in options:
        if option[1] == "E" and option[2] < lowestCost[2]:
            lowestCost = option
    return lowestCost
    
def reverseStep(pos, path, seen, grid):
    seen[pos] = path[pos]
    #find nighbors with lower costs
    options = []
    for x in [-1,0,1]:
        for y in [-1,0,1]:
            if abs(x)+abs(y) == 1:
                if path[addTuple(pos, (x,y))] < path[pos]:
                    options.append((addTuple(pos, (x,y)), path[addTuple(pos, (x,y))]))
    if len(options) > 1:
        pass
    for option in options:
        reverseStep(option[0], path, seen, grid)

def partOne(data):
    data = {(x,y):data[y][x] for y in range(len(data)) for x in range(len(data[y].strip()))}
    start = [x for x in data.keys() if data[x] =="S"][0]
    end = [x for x in data.keys() if data[x] =="E"][0]
    seen  =defaultdict(lambda: 1e20)
    cost = step(start, seen, (1,0), 0, [], data)
    return cost, seen

def partTwo(data, seen):
    data = {(x,y):data[y][x] for y in range(len(data)) for x in range(len(data[y].strip()))}
    start = [x for x in data.keys() if data[x] =="S"][0]
    end = [x for x in data.keys() if data[x] =="E"][0]
    
    #start at the end, and move twoards the start, only taking decreasing paths?
    
    bestCost = seen[end]
    best = {}
    reverseStep(end, seen, best, data)
    bestTiles = set(best.keys())
    
    for stepy in best.keys():
        if stepy == end or stepy == start: 
            continue
        grid = copy.deepcopy(data)
        grid[stepy] = "#"
        newSeen  =defaultdict(lambda: 1e20)
        cost = step(start, newSeen, (1,0), 0, [], grid)[2]
        if stepy == (14,7):
            pass
        if cost == bestCost:
            newBest = {}
            reverseStep(end, newSeen, newBest, grid)
            bestTiles.update(newBest.keys())
    return len(bestTiles)

def main(fileName):
    data = []
    with open(fileName, 'r') as file:
        data = file.readlines()

    start_time = time.time()
    cost, seen = partOne(data)
    print(cost[2])
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    print(partTwo(data, seen))
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', help='use the test input or not', 
                        action='store_false', required=False)
    args = parser.parse_args()
    fileName =join(sys.path[0],( "input" if args.test else "TestInput"))
    main(fileName)
    
    
    
    #([(1, 139), (2, 139), (3, 139), (4, 139), (5, 139), (5, 138), (5, 137), (5, 136), (5, 135), (6, 135), (7, 135), (8, 135), (9, 135), (9, 134), (9, 133), (9, 132), (9, 131), (9, 130), (9, 129), (9, 128), (9, 127), (9, 126), (9, 125), (9, 124), (9, 123), (10, 123), (11, 123), (11, 122), (11, 121), (11, 120), (11, 119), (11, 118), (11, 117), (11, 116), (11, 115), (11, 114), (11, 113), (11, 112), (11, 111), (10, 111), (9, 111), (8, 111), (7, 111), (7, 110), (7, 109), (7, 108), (7, 107), (7, 106), (7, 105), (8, 105), (9, 105), (10, 105), (11, 105), (12, 105), (13, 105), (13, 104), (13, 103), (13, 102), (13, 101), (13, 100), (13, 99), (12, 99), (11, 99), (11, 98), (11, 97), (11, 96), (11, 95), (11, 94), (11, 93), (11, 92), (11, 91), (11, 90), (11, 89), (10, 89), (9, 89), (8, 89), (7, 89), (6, 89), (5, 89), (4, 89), (3, 89), (2, 89), (1, 89), (1, 88), (1, 87), (1, 86), (1, 85), (1, 84), (1, 83), (1, 82), (1, 81), (1, 80), (1, 79), (1, 78), (1, 77), (1, 76), (1, 75), (1, 74), (1, 73), (1, 72), (1, 71), (1, 70), (1, 69), (1, 68), (1, 67), (1, 66), (1, 65), (1, 64), (1, 63), (1, 62), (1, 61), (1, 60), (1, 59), (2, 59), (3, 59), (3, 60), (3, 61), (3, 62), (3, 63), (3, 64), (3, 65), (3, 66), (3, 67), (4, 67), (5, 67), (5, 66), (5, 65), (5, 64), (5, 63), (5, 62), (5, 61), (5, 60), (5, 59), (5, 58), (5, 57), (5, 56), (5, 55), (4, 55), (3, 55), (2, 55), (1, 55), (1, 54), (1, 53), (1, 52), (1, 51), (2, 51), (3, 51), (3, 50), (3, 49), (2, 49), (1, 49), (1, 48), (1, 47), (1, 46), (1, 45), (1, 44), (1, 43), (1, 42), (1, 41), (2, 41), (3, 41), (4, 41), (5, 41), (5, 40), (5, 39), (5, 38), (5, 37), (5, 36), (5, 35), (6, 35), (7, 35), (8, 35), (9, 35), (9, 34), (9, 33), (9, 32), (9, 31), (9, 30), (9, 29), (9, 28), (9, 27), (9, 26), (9, 25), (10, 25), (11, 25), (12, 25), (13, 25), (13, 24), (13, 23), (14, 23), (15, 23), (16, 23), (17, 23), (18, 23), (19, 23), (20, 23), (21, 23), (22, 23), (23, 23), (23, 24), (23, 25), (24, 25), (25, 25), (26, 25), (27, 25), (28, 25), (29, 25), (30, 25), (31, 25), (31, 24), (31, 23), (32, 23), (33, 23), (34, 23), (35, 23), (35, 24), (35, 25), (35, 26), (35, 27), (36, 27), (37, 27), (37, 26), (37, 25), (38, 25), (39, 25), (39, 24), (39, 23), (39, 22), (39, 21), (38, 21), (37, 21), (36, 21), (35, 21), (35, 20), (35, 19), (35, 18), (35, 17), (34, 17), (33, 17), (32, 17), (31, 17), (30, 17), (29, 17), (29, 16), (29, 15), (29, 14), (29, 13), (29, 12), (29, 11), (29, 10), (29, 9), (29, 8), (29, 7), (29, 6), (29, 5), (29, 4), (29, 3), (30, 3), (31, 3), (32, 3), (33, 3), (34, 3), (35, 3), (36, 3), (37, 3), (38, 3), (39, 3), (40, 3), (41, 3), (42, 3), (43, 3), (43, 4), (43, 5), (43, 6), (43, 7), (44, 7), (45, 7), (46, 7), (47, 7), (47, 6), (47, 5), (47, 4), (47, 3), (47, 2), (47, 1), (48, 1), (49, 1), (50, 1), (51, 1), (52, 1), (53, 1), (54, 1), (55, 1), (56, 1), (57, 1), (57, 2), (57, 3), (56, 3), (55, 3), (55, 4), (55, 5), (55, 6), (55, 7), (56, 7), (57, 7), (58, 7), (59, 7), (60, 7), (61, 7), (62, 7), (63, 7), (64, 7), (65, 7), (66, 7), (67, 7), (68, 7), (69, 7), (70, 7), (71, 7), (72, 7), (73, 7), (73, 8), (73, 9), (73, 10), (73, 11), (74, 11), (75, 11), (76, 11), (77, 11), (78, 11), (79, 11), (80, 11), (81, 11), (82, 11), (83, 11), (84, 11), (85, 11), (86, 11), (87, 11), (87, 12), (87, 13), (88, 13), (89, 13), (90, 13), (91, 13), (92, 13), (93, 13), (94, 13), (95, 13), (95, 12), (95, 11), (96, 11), (97, 11), (97, 12), (97, 13), (98, 13), (99, 13), (99, 12), (99, 11), (100, 11), (101, 11), (102, 11), (103, 11), (104, 11), (105, 11), (106, 11), (107, 11), (108, 11), (109, 11), (110, 11), (111, 11), (112, 11), (113, 11), (114, 11), (115, 11), (115, 12), (115, 13), (116, 13), (117, 13), (118, 13), (119, 13), (120, 13), (121, 13), (121, 12), (121, 11), (122, 11), (123, 11), (123, 12), (123, 13), (124, 13), (125, 13), (125, 14), (125, 15), (126, 15), (127, 15), (127, 16), (127, 17), (126, 17), (125, 17), (125, 18), (125, 19), (126, 19), (127, 19), (128, 19), (129, 19), (129, 20), (129, 21), (130, 21), (131, 21), (131, 22), (131, 23), (132, 23), (133, 23), (133, 24), (133, 25), (134, 25), (135, 25), (136, 25), (137, 25), (138, 25), (139, 25), (139, 24), (139, 23), (139, 22), (139, 21), (139, 20), (139, 19), (139, 18), (139, 17), (139, 16), (139, 15), (138, 15), (137, 15), (137, 14), (137, 13), (138, 13), (139, 13), (139, 12), (139, 11), (139, 10), (139, 9), (139, 8), (139, 7), (138, 7), (137, 7), (136, 7), (135, 7), (135, 8), (135, 9), (134, 9), (133, 9), (133, 8), (133, 7), (133, 6), (133, 5), (134, 5), (135, 5), (136, 5), (137, 5), (138, 5), (139, 5), (139, 4), (139, 3), (139, 2)], 'E', 91464)