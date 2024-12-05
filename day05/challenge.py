import time
import argparse
import sys
import copy
from os.path import join
from collections import defaultdict

def partOne(data):
    rules, pages = ''.join(data).split("\n\n")
    
    rulesDict = defaultdict(lambda: [])
    [rulesDict[line[:line.index('|')]].append(line[line.index('|')+1:]) for line in rules.split('\n')]
    pages = [[x for x in set.split(',')] for set in pages.split('\n')]
    
    
    # There are no duplicate pages
    total = 0
    for page in pages:
        valid = True
        for rule in rulesDict.keys():
            if rule in page:
                index = page.index(rule)
                splitList = page[:index]
                rules = rulesDict[rule]
                if not set(splitList).isdisjoint(set(rules)):
                    valid = False
                    break
        if valid:
            total += int(page[int(((len(page)-1)/2))])
    return total

def partTwo(data):
    rules, pages = ''.join(data).split("\n\n")
    
    rulesDict = defaultdict(lambda: [])
    [rulesDict[line[:line.index('|')]].append(line[line.index('|')+1:]) for line in rules.split('\n')]
    pages = [[x for x in set.split(',')] for set in pages.split('\n')]
    
    
    # There are no duplicate pages
    total = 0
    for page in pages:
        valid = True
        for rule in rulesDict.keys():
            if rule in page:
                index = page.index(rule)
                splitList = page[:index]
                rules = rulesDict[rule]
                if not set(splitList).isdisjoint(set(rules)):
                    valid = False
                    # I guess we should move this key to before any rule breaking element?
                    page.pop(page.index(rule))
                    earliestIndex = 100000
                    for elem in rulesDict[rule]:
                        earliestIndex = page.index(elem) if elem in page and page.index(elem) < earliestIndex else earliestIndex
                    page.insert(earliestIndex, rule)
                    pass
        if not valid:
            total += int(page[int(((len(page)-1)/2))])
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