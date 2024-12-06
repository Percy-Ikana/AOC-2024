import time
import argparse
import sys
import copy
from os.path import join
import multiprocessing

def printGrid(bounds, obsticals, positions):
    for y in bounds[1]:
        line = ''
        for x in bounds[0]:
            toPrint = "."
            if (x,y) in obsticals: toPrint = '#'
            if (x,y) in positions: toPrint = 'X'
            line += toPrint
        print(line)

dirs = {
    '^':(0,-1),
    'v':(0,1),
    '<':(-1,0),
    '>':(1,0),
}

rotations = {
    '^':'>',
    '>':'v',
    'v':'<',
    '<':'^',
}

def partOne(data):
    #assuming square
    bounds = (range(0, len(data[0])-1), range(0, len(data)))
    obsticals = {(x, y) for y in range(len(data)) for x in range(len(data[y])) if data[y][x] == '#'}
    start = [((x, y), data[y][x]) for y in range(len(data)) for x in range(len(data[y])) if data[y][x] in '^v<>']
    start = {'position':start[0][0], 'facing':start[0][1]}
    positions = set()
    
    currentPosition = copy.deepcopy(start)
    while True:
        #So we loop, moving the guard in the facing firection until they hit an obstacle
        #We end this when they either leave the map, or return to the same place they started with the same facing
        nextPos = (currentPosition['position'][0] + dirs[currentPosition['facing']][0], currentPosition['position'][1] + dirs[currentPosition['facing']][1])
        
        #is the next position a #?
        if nextPos in obsticals:
            currentPosition['facing'] = rotations[currentPosition['facing']]
        else:
            #append current pos to the list of visited locations
            positions.add(currentPosition['position'])
            #Update position
            currentPosition['position'] = nextPos
        
        #check for end conditions after moving
        if (currentPosition['position'][0] not in bounds[0] or currentPosition['position'][1] not in bounds[1]) or currentPosition == start:
            #we are out of bounds, or we looped
            break
    
    #printGrid(bounds, obsticals, positions)
    
    return positions


def runLoop(newObsticalPosition, bounds, obsticals, start, valid):
    
    currentPosition = copy.deepcopy(start)
    positions = set()
    while True:                
        #So we loop, moving the guard in the facing firection until they hit an obstacle
        #We end this when they either leave the map, or return to the same place they started with the same facing
        
        nextPos = (currentPosition['position'][0] + dirs[currentPosition['facing']][0], currentPosition['position'][1] + dirs[currentPosition['facing']][1])
        
        #is the next position a #?
        if nextPos in obsticals or nextPos == newObsticalPosition:
            currentPosition['facing'] = rotations[currentPosition['facing']]
        else:
            #Update position
            currentPosition['position'] = nextPos
                        
        if (currentPosition['position'], currentPosition['facing']) in positions:
            valid[newObsticalPosition] = True
            return True
        positions.add((currentPosition['position'], currentPosition['facing']))
        
        #check for end conditions after moving
        if (currentPosition['position'][0] not in bounds[0] or currentPosition['position'][1] not in bounds[1]):
            #we are out of bounds, or we looped
            break
    #no loop found
    valid[newObsticalPosition] = False
    return False


def partTwo(data, part1Results):
        #assuming square
    bounds = (range(0, len(data[0])-1), range(0, len(data)))
    obsticals = {(x, y) for y in range(len(data)) for x in range(len(data[y])) if data[y][x] == '#'}
    start = [((x, y), data[y][x]) for y in range(len(data)) for x in range(len(data[y])) if data[y][x] in '^v<>']
    start = {'position':start[0][0], 'facing':start[0][1]}            

    if len(bounds[0])*len(bounds[1]) < 50:
        valid = [runLoop((x,y), bounds, obsticals, start, {})  for y in bounds[1] for x in bounds[0] if (x,y) != start['position'] and (x,y) in part1Results]
        return sum(valid)
    else:
        valid = multiprocessing.Manager().dict({})
        checks = []
        for y in bounds[1]:
            for x in bounds[0]:
                if (x,y) != start['position'] and (x,y) in part1Results:
                    checks.append(((x,y), bounds, obsticals, start, valid))
        p = multiprocessing.Pool()
        p.starmap(runLoop, checks)
        return sum(valid.values())

def main(fileName):
    data = []
    with open(fileName, 'r') as file:
        data = file.readlines()

    start_time = time.time()
    
    pos = partOne(data)
    print(len(pos))
    print(partTwo(data, pos))
    
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', help='use the test input or not', 
                        action='store_false', required=False)
    args = parser.parse_args()
    fileName =join(sys.path[0],( "input" if args.test else "TestInput"))
    main(fileName)