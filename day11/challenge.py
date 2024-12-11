import time
import argparse
import sys
import copy
from os.path import join
import math
from collections import defaultdict

def partOne(data):
    stones = [int(x) for x in data[0].split()]
    
    # part two would obvs work here as well (and be faster)
    # but im keeping this here to preserve my OG solution
    for x in range(25):
        tempStones = []
        for stone in stones:
            if stone == 0:
                tempStones.append(1)
                continue
            numDigits = int(math.log10(stone))+1
            if (numDigits)%2 == 0:
                mid = 10 ** (numDigits//2)

                left = stone // mid
                right = stone % mid
                tempStones.append(left)
                tempStones.append(right)
                continue
            tempStones.append(stone*2024)
        stones = tempStones
    return(len(stones))

def partTwo(data):
    
    #The order of the stones if irrelevant, 
    #All that matters is an indivdidual stones number
    #so we can do operations once, and "apply" it to 
    #all copies of the same number
    stones = {int(stone):1 for stone in data[0].split()}

    for x in range(75):
        tempStones = defaultdict(lambda:0)
        
        for number in stones:
            count = stones[number]

            if number == 0:
                tempStones[1] +=count
                continue
            
            numDigits = int(math.log10(number))+1
            if numDigits % 2 == 0:
                mid = 10 ** (numDigits//2)

                left = number // mid
                right = number % mid
                tempStones[left] += count
                tempStones[right] += count
                continue
            
            tempStones[number*2024] += count
            
        stones = tempStones

    return sum(stones.values())

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