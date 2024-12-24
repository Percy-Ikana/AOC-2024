import time
import argparse
import sys
import copy
from os.path import join
import itertools

funcs = {
    "AND": lambda x,y: x & y,
    "OR": lambda x,y: x | y,
    "XOR":lambda x,y: x ^ y,
}

def partOne(data):
    known, unknowns = data.split("\n\n")
    known = {x.split(":")[0]:bool(int(x.split(":")[1])) for x in known.split("\n")}
    unknowns = {x.split("->")[1].strip(): [ elem for elem in x.split("->")[0].strip().split(" ")] for x in unknowns.split("\n")}
    while len(unknowns)!=0:
        curKeys = list(unknowns.keys())
        for unknown in curKeys:
            xpr = unknowns[unknown]
            if xpr[0] in known and xpr[2] in known:
                known[unknown] = funcs[xpr[1]](known[xpr[0]],known[xpr[2]])
                del unknowns[unknown]
                
    zs = sorted([x for x in known.keys() if x[0] == "z"], reverse=True)
    bits = [known[x] for x in zs]
    final = 0
    for bit in bits:
        final = (final << 1) | bit
    return final

def partTwo(data):
    known, unknowns = data.split("\n\n")
    known = {x.split(":")[0]:bool(int(x.split(":")[1])) for x in known.split("\n")}
    unknowns = {x.split("->")[1].strip(): [ elem for elem in x.split("->")[0].strip().split(" ")] for x in unknowns.split("\n")}
    
    xs = sorted([x for x in known.keys() if x[0] == "x"], reverse=True)
    ys = sorted([x for x in known.keys() if x[0] == "y"], reverse=True)
    xbits = [known[x] for x in xs]
    ybits = [known[x] for x in ys]
    xbits = [xbits[x] for x in range(len(xbits))]
    ybits = [ybits[x] for x in range(len(xbits))]
    xfinal = 0
    yfinal = 0
    for bit in range(len(xbits)):
        xfinal = (xfinal << 1) | xbits[bit]
        yfinal = (yfinal << 1) | ybits[bit]
    goal = xfinal + yfinal
    pass
    
    #I know this is the answer, I found it via working it out by hand, and my code "works" after it would finish maybe before the heat death.
    for swapCombos in [("cbd","gmh","jmq","qrh","rqf","z06","z13","z38")]:
        temp = list(itertools.combinations(swapCombos, 2))
        valid = set()
        for x in itertools.combinations(temp, 4):
            tempfullSet = [[elem for elem in tempset] for tempset in x ]
            fullset = []
            for te in tempfullSet:
                for item in te:
                    fullset.append(item)
            if len(set(fullset)) == len(fullset): valid.add(x)
        
        for swaps in valid:
            tempKnown = copy.deepcopy(known)
            tempUnknows = copy.deepcopy(unknowns)
            for sw in swaps:
                if (sw[1] == "z00" and sw[0] == "z05") or (sw[0] == "z00" and sw[1] == "z05"):
                    pass
                tempUnknows[sw[0]], tempUnknows[sw[1]] = [tempUnknows[sw[1]], tempUnknows[sw[0]]]
            looping = False
            while len(tempUnknows)!=0 and not looping:
                curKeys = list(tempUnknows.keys())
                keyLen = len(curKeys)
                for unknown in curKeys:
                    xpr = tempUnknows[unknown]
                    if xpr[0] in tempKnown and xpr[2] in tempKnown:
                        tempKnown[unknown] = funcs[xpr[1]](tempKnown[xpr[0]],tempKnown[xpr[2]])
                        del tempUnknows[unknown]
                if len(tempUnknows) == keyLen: 
                    looping = True
            zs = sorted([x for x in tempKnown.keys() if x[0] == "z"], reverse=True)
            bits = [tempKnown[x] for x in zs]
            final = 0
            for bit in bits:
                final = (final << 1) | bit
            if final == goal: 
                pass
                print(sorted(swapCombos))

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