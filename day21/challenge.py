import time
import argparse
import sys
import copy
from os.path import join
from collections import Counter
import heapq

keyGrid = {c: (i % 3, i // 3) for i, c in enumerate("789456123 0A")}
counterGrid = {c: (i % 3, i // 3) for i, c in enumerate(" ^A<v>")}


def steps(controls, instructions, count=1):
    startX, startY = controls["A"]
    emptyX, emptyY = controls[" "]
    results = Counter()
    for c in instructions:
        instX, instY = controls[c]
        #Check if we would pass over the empty square, if yes, mark thi inst for flipping the order.
        f = instX == emptyX and startY == emptyY or instY == emptyY and startX == emptyX
        results[(instX - startX, instY - startY, f)] += count
        startX, startY = instX, instY
    return results


def inputSim(inputs, robots):
    r = 0
    for input in inputs:
        res = steps(keyGrid, input)
        for _ in range(robots+1):
            pass
            total = []
            for x,y, flip in res:
                #we want to move far away first, since we want the last move to be closest to A, 
                #Although we have to do the other order if the best order passes over the panic square
                string = ("<" * -x + "v" * y + "^" * -y + ">" * x)
                string = string[:: -1 if flip else 1] + "A"
                path = steps(counterGrid, string, res[(x, y, flip)])
                total.append(path)
            res = sum(total, Counter())
        r += res.total() * int(input[:3])
    return r
# Keypad = robot -> remote = robot -> remote = robot -> remote = human
def partOne(data):
    inputs = [line.strip() for line in data]

    return inputSim(inputs, 2)

def partTwo(data):
    inputs = [line.strip() for line in data]

    return inputSim(inputs, 25)

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