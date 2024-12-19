import time
import argparse
import sys
import copy
from os.path import join
from collections import defaultdict
import heapq

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

def partOne(data, bounds, steps):
    grid = defaultdict(lambda:"#", {(x,y):"." for y in bounds for x in bounds})
    walls = {(int(data[line].split(",")[0]), int(data[line].split(",")[1])):"#" for line in range(len(data)) if line < steps}
    grid = grid | walls | {(len(bounds)-1, len(bounds)-1) : "E"}
    adjacency = {}
    currentKeys = list(grid.keys())
    for item in currentKeys:
        adjacency[item] = {(item[0]+x, item[1]+y):1 for x in [-1,0,1] for y in [-1,0,1] if abs(x)+abs(y) == 1 and grid[(item[0]+x, item[1]+y)] != "#"}
    dist, paths = dijkstra(adjacency, (0,0))
    return dist[(len(bounds)-1, len(bounds)-1)]

def partTwo(data, bounds, steps):
    last = 0
    for x in range(steps,len(data)):
        grid = defaultdict(lambda:"#", {(x,y):"." for y in bounds for x in bounds})
        walls = {(int(data[line].split(",")[0]), int(data[line].split(",")[1])):"#" for line in range(len(data)) if line < x}
        grid = grid | walls | {(len(bounds)-1, len(bounds)-1) : "E"}
        adjacency = {}
        currentKeys = list(grid.keys())
        for item in currentKeys:
            adjacency[item] = {(item[0]+x, item[1]+y):1 for x in [-1,0,1] for y in [-1,0,1] if abs(x)+abs(y) == 1 and grid[(item[0]+x, item[1]+y)] != "#"}
        dist, paths = dijkstra(adjacency, (0,0))
        if dist[(len(bounds)-1, len(bounds)-1)] == float('inf'):
            last = x
            break
    return data[last-1]

def main(fileName, bounds, steps):
    data = []
    with open(fileName, 'r') as file:
        data = file.readlines()

    start_time = time.time()
    
    print(partOne(data, bounds, steps))
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    print(partTwo(data, bounds, steps))
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', help='use the test input or not', 
                        action='store_false', required=False)
    args = parser.parse_args()
    fileName =join(sys.path[0],( "input" if args.test else "TestInput"))
    bounds = range(71) if args.test else range(7)
    steps = 1024 if args.test else 12
    main(fileName, bounds, steps)