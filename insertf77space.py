import sys
from shutil import copyfile
import argparse
import varlibs as vl

parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument('--ff77', dest="fold", type=str, nargs=1, default=[""],
    help='the fortran 77 file to be procssed')

args = parser.parse_args()

f77f=args.fold[0]

frpt=f77f+'.insrt'
fwr = open(frpt, "w")

with open(f77f,'r') as foldf:
    line = foldf.readline()
    while line:
        
        if line[0:2]=='  ' or line[0:2] == 'C ' \
            or line[0:2] == 'C-' or line.strip()=='C' \
            or vl.is_digit(line[0:2]):
            fwr.write(line.rstrip()+'\n')
        else:
            if vl.is_digit(line[0]):
                fwr.write('     '+line.rstrip()+'\n')
            else:    
                fwr.write('      '+line.rstrip()+'\n')
        line = foldf.readline()


fwr.close()                