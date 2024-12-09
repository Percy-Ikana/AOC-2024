import time
import argparse
import sys
import copy
from os.path import join
from collections import defaultdict

def recurse(index, list, total, target, ops, concat = False):
    if index == len(list):
        return total == target

    prod = recurse(index+1, list, total*list[index], target, f'{ops} * {list[index]}', concat)
    sum = recurse(index+1, list, total+list[index], target, f'{ops} + {list[index]}', concat)
    con = recurse(index+1, list, int(str(total)+str(list[index])), target, f'{ops} || {list[index]}', concat) if concat else False

    return prod or sum or con

def partOne(data):
    info = defaultdict(lambda:[])
    { info[int(line.split(":")[0])].append([int(x) for x in line.split(":")[1].split()]) for line in data}
    valid = []
    for line in info.keys():
        for set in info[line]:
            if recurse(1, set, set[0], line, f'{line} : {set[0]}'):
                valid.append(line)
    return sum(valid)

def partTwo(data):
    info = defaultdict(lambda:[])
    { info[int(line.split(":")[0])].append([int(x) for x in line.split(":")[1].split()]) for line in data}
    valid = []
    for line in info.keys():
        for set in info[line]:
            if recurse(1, set, set[0], line, f'{line} : {set[0]}', True):
                valid.append(line)
    return sum(valid)

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