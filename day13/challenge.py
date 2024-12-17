import time
import argparse
import sys
import copy
from os.path import join
import re


def solve(data, mod=0):
    total = 0
    for system in data:
        ax = system[0][0]
        ay = system[0][1]
        
        bx = system[1][0]
        by = system[1][1]
        
        gx = system[2][0] + mod
        gy = system[2][1] + mod
        
        slopeA = ay/ax
        yInterceptA = gy - slopeA * gx

        slopeB = by/bx
        yInterceptB = 0
        
        xIntersection = (yInterceptB - yInterceptA) / (slopeA - slopeB)
        
        bCount = xIntersection / bx
        aCount = (gx -xIntersection) / ax
        
        
        if abs(aCount - round(aCount)) < .001 and abs(bCount - round(bCount)) < .001:
            total+=round(aCount)*3 + round(bCount)
        
        
    return total

def parse(data):
    data = [set.split('\n') for set in data.split("\n\n")]
    for set in data:
        set[0] = [int(re.search("X\\+(.*), Y+", set[0]).group(1)), int(re.search("Y\\+(.*)", set[0]).group(1))]
        set[1] = [int(re.search("X\\+(.*), Y+", set[1]).group(1)), int(re.search("Y\\+(.*)", set[1]).group(1))]
        set[2] = [int(re.search("X=(.*), Y=", set[2]).group(1)), int(re.search("Y=(.*)", set[2]).group(1))]
    return data

def partOne(data):
    data = parse(data)
    
    return solve(data)

def partTwo(data):
    data = parse(data)
    
    return solve(data, 10000000000000)

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
