import time
import argparse
import sys
import copy
from collections import defaultdict
from collections import Counter
from os.path import join

def partOne(data):
    list1, list2 = [], []
    for line in data:
        splits = line.strip().split('   ')
        list1.append(int(splits[0]))
        list2.append(int(splits[1]))
    list1.sort()
    list2.sort()
    return (sum([abs(list1[x] - list2[x]) for x in range(len(list1))]))

def partTwo(data):
    list1, list2 = [], []
    for line in data:
        splits = line.strip().split('   ')
        list1.append(int(splits[0]))
        list2.append(int(splits[1]))
    list1 = Counter(list1)
    list2 = Counter(list2)
    total = 0
    for number in list1.keys():
        total += list1[number] * list2[number] * number
    return total

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