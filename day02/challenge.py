import time
import argparse
import sys
import copy
from os.path import join
from functools import reduce

def partOne(data):
    data = [[int(x) for x in line.split()] for line in data]
    results = []
    for line in data:
        safe = True
        diffSign = (line[0] - line[1])/abs((line[0] - line[1])) if (line[0] - line[1])!= 0 else 0
        for elem in range(len(line)-1):
            diff = abs(line[elem] - line[elem+1])
            currDiffDign = (line[elem] - line[elem+1])/abs((line[elem] - line[elem+1])) if (line[elem] - line[elem+1]) != 0 else 0
            if diff not in range(1,4) or diffSign != currDiffDign or diffSign == 0:
                safe = False
                break
        results.append(safe)
    return sum([1 for x in results if x])

def partTwo(data):
    data = [[int(x) for x in line.split()] for line in data]
    results = []
    for line in data:
        tempResults = []
        for possibility in range(len(line)):
            newLine = copy.deepcopy(line)
            newLine.pop(possibility)
            safe = True
            diffSign = (newLine[0] - newLine[1])/abs((newLine[0] - newLine[1])) if (newLine[0] - newLine[1])!= 0 else 0
            for elem in range(len(newLine)-1):
                diff = abs(newLine[elem] - newLine[elem+1])
                currDiffDign = (newLine[elem] - newLine[elem+1])/abs((newLine[elem] - newLine[elem+1])) if (newLine[elem] - newLine[elem+1]) != 0 else 0
                if diff not in range(1,4) or diffSign != currDiffDign or diffSign == 0:
                    safe = False
                    break
            tempResults.append(safe)
        results.append(any(tempResults))
    return sum([1 for x in results if x])

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