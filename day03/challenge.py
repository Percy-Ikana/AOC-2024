import time
import argparse
import sys
import copy
from os.path import join
import re 

def partOne(data):
    data = ''.join(data)
    matches = re.findall("mul\([0-9]*,[0-9]*\)", data)
    products = [int(match[4:match.index(',')]) * int(match[match.index(',') + 1: match.index(')')])  for match in matches]
    return(sum(products))

def partTwo(data):
    data = ''.join(data)
    matches = re.findall("mul\([0-9]*,[0-9]*\)", data)
    
    matchIndexes = [data.find(x) for x in matches]
    doIndexs = [0] + [m.start() for m in re.finditer('do()', data)]
    dontIndexs = [-1] + [m.start() for m in re.finditer("don't()", data)]
    
    products = []
    for match in range(len(matchIndexes)):
        lastDo = [x for x in doIndexs if x < matchIndexes[match]][-1]
        lastDont = [x for x in dontIndexs if x < matchIndexes[match]][-1]
        if lastDo > lastDont:
            products.append(int(matches[match][4:matches[match].index(',')]) * int(matches[match][matches[match].index(',') + 1: matches[match].index(')')]))
    
    return(sum(products))

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