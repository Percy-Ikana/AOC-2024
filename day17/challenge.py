import time
import argparse
import sys
import copy
from os.path import join
import multiprocessing

class AOCComputer:
    a = 0
    b = 0
    c = 0
    program = []
    instPointer = 0

    output = []

    def __init__(self, a,b,c,program):
        self.a = a
        self.b = b
        self.c = c
        self.program = program
        self.output = []
        self.instPointer = 0

    def comboToValue(self, op):
        if op in [0,1,2,3]: return op
        if op == 4: return self.a
        if op == 5: return self.b
        if op == 6: return self.c
        if op == 7: raise Exception

    def adv(self, op):
        self.a = self.a//(2**self.comboToValue(op))
        
    def bxl(self,op):
        self.b = self.b ^ op

    def bst(self,op):
        self.b = self.comboToValue(op) % 8
        
    def jnz(self,op):
        if self.a == 0: return
        self.instPointer = op - 2
        
    def bxc(self,op):
        self.b = self.b ^ self.c
            
    def out(self,op):
        self.output.append(self.comboToValue(op)%8)
        
    def bdv(self,op):
        self.b = self.a//(2**self.comboToValue(op))
        
    def cdv(self,op):
        self.c = self.a//(2**self.comboToValue(op))
        
        
    opToFunc = {
        0: adv,
        1:bxl,
        2:bst,
        3:jnz,
        4:bxc,
        5:out,
        6:bdv,
        7:cdv
    }
    
    def runProgram(self, checkRange = 0):
        initalA = self.a
        while self.instPointer+1 < len(self.program):
            self.opToFunc[self.program[self.instPointer]](self,self.program[self.instPointer+1])
            self.instPointer += 2
            

        if checkRange != 0:
            #same for the program
            partialProg = self.program[checkRange:]
            if partialProg == self.output:
                return True
        return False
    
    def outputOutput(self):
        strOut = map(str, self.output)
        return ",".join(strOut)

def partOne(data):
    a = int(data[0].split(":")[1])
    b = int(data[1].split(":")[1])
    c = int(data[2].split(":")[1])
    program = list(map(int, data[4].split(':')[1].split(",")))
    
    comp  = AOCComputer(a,b,c, program)
    comp.runProgram()
    return comp.outputOutput()

def partTwo(data):
    program = list(map(int, data[4].split(':')[1].split(",")))
    
    mod = 0
    for x in range(1,len(program)+1):
        for i in range(0,10000):
            comp = AOCComputer(mod+i, 0,0, program)
            if comp.runProgram(x*-1):
                mod = (mod+i)*8
                #print(i)
                break
    return mod//8

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