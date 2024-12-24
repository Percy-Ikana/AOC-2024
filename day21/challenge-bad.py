import time
import argparse
import sys
import copy
from os.path import join
from collections import defaultdict
import heapq

keypadAdjacency = {}
keypadAdjacencyHumanReadable = defaultdict(dict)
controlAdjacencyHumanReadable = defaultdict(dict)
controlAdjacency = {}

def dijkstra(adj_list, start):
    distances = {node: float('inf') for node in adj_list}
    distances[start] = 0
    predecessors = {node: None for node in adj_list}  # Track predecessors

    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in adj_list[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node  # Update predecessor
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, predecessors

def get_path(predecessors, start, end):
    path = []
    current_node = end
    while current_node is not None:
        path.insert(0, current_node)
        current_node = predecessors[current_node]

    if path[0] == start:
        return path
    else:
        return None  # No path found

def addTuple(tupe1, tupe2):
    return (tupe1[0] + tupe2[0], tupe1[1] + tupe2[1])

def subTuple(tupe1, tupe2):
    return (tupe1[0] - tupe2[0], tupe1[1] - tupe2[1])

def moves_to(start, end, adj, toGrid):
    route = get_path(dijkstra(adj, toGrid[start])[1], toGrid[start], toGrid[end])
    temp = []
    for elem in range(1,len(route)):
        temp.append(subTuple(route[elem], route[elem-1]))
    return route, temp, [moveToDir[x] for x in temp]

'''
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
'''
gridToKeypad = {
    (0,0):"7",
    (1,0):"8",
    (2,0):"9",
    (0,1):"4",
    (1,1):"5",
    (2,1):"6",
    (0,2):"1",
    (1,2):"2",
    (2,2):"3",
    (1,3):"0",
    (2,3):"A"
}

KeypadToGrid = {
    "7":(0,0),
    "8":(1,0),
    "9":(2,0),
    "4":(0,1),
    "5":(1,1),
    "6":(2,1),
    "1":(0,2),
    "2":(1,2),
    "3":(2,2),
    "0":(1,3),
    "A":(2,3)
}

keypadValues = {
    "<":1,
    "^":2,
    "v":3,
    ">":4
}

'''
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
'''
gridToControl = {
    (1,0):"^",
    (2,0):"A",
    (0,1):"<",
    (1,1):"v",
    (2,1):">"
}

controlToGrid = {
    "^":(1,0),
    "A":(2,0),
    "<":(0,1),
    "v":(1,1),
    ">":(2,1)
}

controlValues = {
    "<":1,
    "^":2,
    "v":3,
    ">":4
}

dirToMove = {
    "^":(0,-1),
    "<":(-1,0),
    ">":(1,0),
    "v":(0,1)
}

moveToDir = {
    (0,-1):"^",
    (-1,0):"<",
    (1,0):">",
    (0,1):"v"
}

# Keypad = robot -> remote = robot -> remote = robot -> remote = human
def partOne(data):
    inputs = [list(line.strip()) for line in data]
    #so, every input on a control starts at A and ands at A, right?


    for item in gridToKeypad.keys():
        keypadAdjacency[item] = {(item[0]+x, item[1]+y):1 for x in [-1,0,1] for y in [-1,0,1] if abs(x)+abs(y) == 1 and (item[0]+x, item[1]+y) in gridToKeypad}
    
    for button in keypadAdjacency:
        for x in keypadAdjacency[button]:
            keypadAdjacencyHumanReadable[gridToKeypad[button]][gridToKeypad[x]] = 1

    
    for item in gridToControl.keys():
        controlAdjacency[item] = {(item[0]+x, item[1]+y):1 for x in [-1,0,1] for y in [-1,0,1] if abs(x)+abs(y) == 1 and (item[0]+x, item[1]+y) in gridToControl}
    
    for button in controlAdjacency:
        for x in controlAdjacency[button]:
            controlAdjacencyHumanReadable[gridToControl[button]][gridToControl[x]] = 1

    numRobots = 1
    sequence = {}
    for input in inputs:
        #if input != list("379A"): continue
        keyPadStart = "A"
        robot1Start = "A"
        robot2Start = "A"

        robot1Path = []
        for press in input:
            #get the presses to go from the start, to the destination
            res = moves_to(keyPadStart, press, keypadAdjacency, KeypadToGrid)
            #okay, now the second robot, needs to take these inputs, and 
            keyPadStart = press
            robot1Path.append(''.join(res[2]))
        robot1Path = [''.join(sorted(x, key=lambda char:keypadValues[char])) for x in robot1Path]
        robot1Path = "A".join(robot1Path) + "A"
        #print("".join(robot1Path))

        for _ in range(numRobots+1):
            robot2Path = []
            for press in robot1Path:
                res = moves_to(robot1Start, press, controlAdjacency, controlToGrid)
                robot1Start = press
                robot2Path.append(''.join(res[2]))
            robot2Path = [''.join(sorted(x, key=lambda char:controlValues[char])) for x in robot2Path]
            robot2Path = "A".join(robot2Path) + "A"
            #print("".join(robot2Path))
            robot1Path = robot2Path

        sequence[''.join(input)] = "".join(robot1Path)
    [print(f"{x}:{sequence[x]}") for x in sequence]
    return sum([int(x[:3])*len(sequence[x]) for x in sequence])

def partTwo(data):
    pass

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