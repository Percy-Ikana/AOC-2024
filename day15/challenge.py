import time
import argparse
import sys
import copy
from os.path import join

instToMove = {
    '<': (-1,0),
    '>': (1,0),
    'v': (0,1),
    '^': (0,-1),
}

def addTuple(tupe1, tupe2):
    return (tupe1[0] + tupe2[0], tupe1[1] + tupe2[1])

def printGrid(data, robot, bounds):
    for y in range(bounds[1]):
        line = ""
        for x in range(bounds[0]):
            char  = data[(x,y)] if (x,y) in data else " "
            char = "@" if (x,y) == robot else char
            line = line + char
        print(line)

def partOne(data):
    grid, instructions = data.split("\n\n")
    grid = grid.split()
    start = list({(x, y) : grid[y][x] for y in range(len(grid)) for x in range(len(grid[y].strip())) if grid[y][x] == '@' }.keys())[0]
    bounds = (len(grid[0].strip()), len(grid))
    grid = {(x, y) : grid[y][x] for y in range(len(grid)) for x in range(len(grid[y].strip())) if grid[y][x] != '.' and grid[y][x] != '@' }
    
    instructions = ''.join(instructions.split())
    for intruction in instructions:
        dir = instToMove[intruction]
        lookPos = addTuple(start, dir)
        if lookPos not in grid:
            start = lookPos
        elif grid[lookPos] == "#":
            pass
        else:
            #We hit a box! so find all boxes before the next all, or dead space
            boxes = []
            end = False
            move = True
            lookAhead = lookPos
            while not end:
                boxes.append(lookAhead)
                lookAhead = addTuple(lookAhead, dir)
                if lookAhead in grid and grid[lookAhead] == "#":
                    move = False
                    break
                end = not lookAhead in grid
                if end:
                    boxes.append(lookAhead)
            if move:
                boxes.reverse()
                for box in boxes:
                    grid[box] = "O"
                del grid[boxes[-1]]
                start = lookPos
                pass
        #printGrid(grid, start, bounds)
    boxes = [100*key[1] + key[0] for key in grid if grid[key] == "O"]
    return(sum(boxes))

def appendDict(x,y, char, char2, dict):
    dict[(x*2, y)] = char
    dict[((x*2)+1, y)] = char2

def partTwo(data):
    grid, instructions = data.split("\n\n")
    grid = grid.split()
    start = list({(x*2, y) : grid[y][x] for y in range(len(grid)) for x in range(len(grid[y].strip())) if grid[y][x] == '@' }.keys())[0]
    bounds = (len(grid[0].strip())*2, len(grid))
    walls = {}
    nothing = {}
    [appendDict(x,y, '#', '#', walls) for y in range(len(grid)) for x in range(len(grid[y].strip())) if grid[y][x] == '#' ]
    boxes = {}
    [appendDict(x,y, '[', ']', boxes) for y in range(len(grid)) for x in range(len(grid[y].strip())) if grid[y][x] == 'O' ]
    [appendDict(x,y, '.', '.', nothing) for y in range(len(grid)) for x in range(len(grid[y].strip())) if grid[y][x] == '.' ]
    grid = walls | boxes | nothing | {start:".", addTuple(start, (1,0)):"."}
    #printGrid(grid, start, bounds)

    instructions = ''.join(instructions.split())
    for intruction in instructions:
        dir = instToMove[intruction]
        lookPos = addTuple(start, dir)
        if grid[lookPos] == ".":
            start = lookPos
        elif grid[lookPos] == "#":
            pass
        else:
            if intruction in "<>": # same behavior if L/R
                #We hit a box! so find all boxes before the next all, or dead space
                boxes = []
                end = False
                move = True
                lookAhead = lookPos
                while not end:
                    boxes.append(lookAhead)
                    lookAhead = addTuple(lookAhead, dir)
                    if grid[lookAhead] == "#":
                        move = False
                        break
                    end = grid[lookAhead] == "."
                    if end:
                        boxes.append(lookAhead)
                if move:
                    boxes.reverse()
                    for box in range(len(boxes[:-1])):
                        grid[boxes[box]] = grid[boxes[box+1]]
                    grid[boxes[-1]] = '.'
                    start = lookPos
            else:
                boxes = []
                end = False
                move = True
                
                lookAhead = []
                if grid[lookPos] == "[":
                    lookAhead.append(lookPos)
                    lookAhead.append(addTuple(lookPos, (1,0)))
                if grid[lookPos] == "]":
                    lookAhead.append(lookPos)
                    lookAhead.append(addTuple(lookPos, (-1,0)))

                while not end:
                    
                    [boxes.append(look) for look in lookAhead]
                    #here the the doubling logic IG
                    lookAhead = list({addTuple(look, dir) for look in lookAhead})
                    newLookAhead = []
                    for look in lookAhead:
                        if grid[look] == ".": 
                            #appending to the list here was the bug, it would cause psuhes that should not happen.
                            #Not noticitng this was very silly
                            pass
                        if grid[look] == "[":
                            newLookAhead.append(look)
                            newLookAhead.append(addTuple(look, (1,0)))
                        if grid[look] == "]":
                            newLookAhead.append(look)
                            newLookAhead.append(addTuple(look, (-1,0)))
                        if grid[look] == "#":
                            newLookAhead.append(look)
                    lookAhead = list({look for look in newLookAhead})
                    
                    if any([grid[look] == "#" for look in lookAhead]):
                        move = False
                        break


                    end = not any(grid[look] != "." for look in lookAhead)
                    #print(''.join([grid[look] for look in lookAhead]))
                    pass

                    #if end:
                    #    [boxes.append(look) for look in lookAhead]
                if move:
                    boxes.reverse()
                    while len(boxes) != 0:
                        movepositions = [boxes[0]]
                        if grid[boxes[0]] == "]":
                            movepositions.append(addTuple(boxes[0], (-1,0)))
                        if grid[boxes[0]] == "[":
                            movepositions.append(addTuple(boxes[0], (1,0)))
                        for move in movepositions:
                            grid[addTuple(move, dir)] = grid[move]
                            #printGrid(grid, start, bounds)
                            grid[move] = "."
                            #printGrid(grid, start, bounds)
                        [boxes.remove(move) for move in movepositions if move in boxes]

                    start = lookPos
        #print(intruction)    
        #printGrid(grid, start, bounds)
        #time.sleep(.1)
        pass


    boxes = [100*key[1] + key[0] for key in grid if grid[key] == "["]
    return(sum(boxes))

def main(fileName):
    data = []
    with open(fileName, 'r') as file:
        data = file.read()

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