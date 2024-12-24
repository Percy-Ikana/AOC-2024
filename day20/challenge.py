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

def partOne(data):
    grid = defaultdict(lambda: "#", {(x,y):data[y][x] for y in range(len(data)) for x in range(len(data[y].strip()))})
    start = [x for x in grid if grid[x] == "S"][0]
    end = [x for x in grid if grid[x] == "E"][0]
    adjacency = {}
    currentKeys = list(grid.keys())
    for item in currentKeys:
        adjacency[item] = {(item[0]+x, item[1]+y):1 for x in [-1,0,1] for y in [-1,0,1] if abs(x)+abs(y) == 1 and grid[(item[0]+x, item[1]+y)] != "#"}
    dist, paths = dijkstra(adjacency, start)
    path = get_path(paths, start, end)
    base = dist[end]
    shortcuts = {}
    for wall in grid:
        temp = grid[wall]
        if not grid[wall] == "#": continue
        grid[wall] = "."
        for item in currentKeys:
            adjacency[item] = {(item[0]+x, item[1]+y):1 for x in [-1,0,1] for y in [-1,0,1] if abs(x)+abs(y) == 1 and grid[(item[0]+x, item[1]+y)] != "#"}
        dist, paths = dijkstra(adjacency, start)
        newDist = dist[end]
        grid[wall] = temp
        if newDist < base:
            shortcuts[wall] = base - newDist
    return len([x for x in shortcuts if shortcuts[x] >= 100])

def partOneBackport(data):
    grid = defaultdict(lambda: "#", {(x,y):data[y][x] for y in range(len(data)) for x in range(len(data[y].strip()))})
    start = [x for x in grid if grid[x] == "S"][0]
    end = [x for x in grid if grid[x] == "E"][0]
    adjacency = {}
    currentKeys = list(grid.keys())
    for item in currentKeys:
        adjacency[item] = {(item[0]+x, item[1]+y):1 for x in [-1,0,1] for y in [-1,0,1] if abs(x)+abs(y) == 1 and grid[(item[0]+x, item[1]+y)] != "#"}
    dist, paths = dijkstra(adjacency, start)
    path = get_path(paths, start, end)
    
    sum = 0
    for i in range(len(path)):
        for j in range(i + 1, len(path)):
            dist = abs(path[j][0] - path[i][0]) + abs(path[j][1] - path[i][1])
            if dist == 2 and (j - i) - dist >= 100:
                sum += 1
    return sum

def partTwo(data):
    grid = defaultdict(lambda: "#", {(x,y):data[y][x] for y in range(len(data)) for x in range(len(data[y].strip()))})
    start = [x for x in grid if grid[x] == "S"][0]
    end = [x for x in grid if grid[x] == "E"][0]
    adjacency = {}
    currentKeys = list(grid.keys())
    for item in currentKeys:
        adjacency[item] = {(item[0]+x, item[1]+y):1 for x in [-1,0,1] for y in [-1,0,1] if abs(x)+abs(y) == 1 and grid[(item[0]+x, item[1]+y)] != "#"}
    dist, paths = dijkstra(adjacency, start)
    path = get_path(paths, start, end)
    
    sum = 0
    for i in range(len(path)):
        for j in range(i + 1, len(path)):
            dist = abs(path[j][0] - path[i][0]) + abs(path[j][1] - path[i][1])
            if dist <= 20 and (j - i) - dist >= 100:
                sum += 1
    return sum
    

def main(fileName):
    data = []
    with open(fileName, 'r') as file:
        data = file.readlines()

    start_time = time.time()
    
    print(partOneBackport(data))
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