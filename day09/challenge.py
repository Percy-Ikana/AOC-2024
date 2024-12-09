import time
import argparse
import sys
import copy
from os.path import join

def partOne(data):
    data = data[0]
    hdd, numLocations, emptyLocations = [], [], []
    fileId, index = 0, 0
    #freespace is -1
    for elem in range(len(data)):
        if int(elem) % 2 == 0:
            for x in range(int(data[elem])):
                hdd.append(fileId)
                numLocations.append(index)
                index+=1
            fileId += 1
        else:
            for x in range(int(data[elem])):
                hdd.append(-1)
                emptyLocations.append(index)
                index+=1
    
    numLocations.reverse()
    # so we have all full locations, and all empty locaitons, we should be able to move through the empty locaitons, filling them with the full ones, until the empty locations are past all the full ones?
    while emptyLocations[0] < numLocations[0]:
        hdd[emptyLocations[0]] = hdd[numLocations[0]]
        hdd[numLocations[0]] = -1
        emptyLocations.append(numLocations.pop(0))
        numLocations.append(emptyLocations.pop(0))
    
    return sum([segment*hdd[segment] for segment in numLocations])

def partTwo(data):
    data = data[0]
    hdd, numRanges, emptyRanges = [], [], []
    fileId, index = 0, 0
    #freespace is -1
    for elem in range(len(data)):
        if int(elem) % 2 == 0:
            if int(data[elem]) != 0:
                numRanges.append([x for x in range(index, int(data[elem]) + index)])
            else: print("we have a no file")
            for x in range(int(data[elem])):
                hdd.append(fileId)
                index+=1
            fileId += 1
        else:
            if int(data[elem]) != 0:
                emptyRanges.append([x for x in range(index, int(data[elem]) + index)])
            for _ in range(int(data[elem])):
                hdd.append(-1)
                index+=1
    
    numRanges.reverse()
    
    for file in numRanges:
        #We start from the end, and look at ranges from the right
        for empty in emptyRanges:
            if len(empty) >= len(file):
                if file[0] > empty[0]:
                    # we fit! so insert
                    for val in file:
                        hdd[empty.pop(0)] = hdd[val]
                        hdd[val] = -1
                    if len(empty) == 0: emptyRanges.pop(emptyRanges.index(empty))
                    break
                else:
                    break
    
    return sum([segment*hdd[segment] if hdd[segment] != -1 else 0 for segment in range(len(hdd))])



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