import time
import argparse
import sys
import copy
from os.path import join
from functools import cache

part1Result = []

@cache
def mix(num1, num2):
    return num1^num2
@cache
def prune(num):
    return num % 16777216
@cache
def seq1(num):
    return prune(mix(num, num*64))
@cache
def seq2(num):
    return prune(mix(num, num//32))
@cache
def seq3(num):
    return prune(mix(num, num*2048))

@cache
def sequence(num):
    return seq3(seq2(seq1(num)))

def partOne(data):
    global part1Result
    data = map(int, data)
    results = []
    for line in data:
        secret = line
        for _ in range(2000):
           line = sequence(line) 
        results.append(line)
    part1Result = results
    
    return sum(results)

def partTwo(data):
    data = map(int, data)
    results = []
    for line in data:
        secret = line
        monkeyDict = [secret%10]
        for _ in range(2000):
           secret = sequence(secret)
           monkeyDict.append(secret%10)
        results.append(monkeyDict)

    changes = [[line[elem] - line[elem-1] for elem in range(1,len(line))] for line in results]
    
    sequences = {}
    for eme1 in range(len(changes)):
        list = changes[eme1]
        seen = set()
        for elem in range(4,len(list)):
            sequence4 = (list[elem-4], list[elem-3], list[elem-2], list[elem-1])
            if sequence4 not in seen:
                sequences[sequence4] = sequences.get(sequence4, 0) + results[eme1][elem]
            seen.add(sequence4)
    
    sequence4 = max(sequences, key=sequences.get)
    return sequences[sequence4]

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