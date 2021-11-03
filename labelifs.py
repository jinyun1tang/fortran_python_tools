
import numpy as np
import argparse
import sys
#
# globals

def is_comment(tline):
   return tline[0]=='C'


def newIF(label):

    return label+10

def is_a_newif(line):
    tline=line.upper()
    return (tline.find('THEN')>=6)

def is_endif(line):
    tline=line.upper()
    return (tline.find('ENDIF')>=6)


parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument('--ff77', dest="fold", type=str, nargs=1, default=[""],
  help='the fortran 77 file to be labeled')

args = parser.parse_args()

f77f=args.fold[0]

f77lb=f77f+'.lbif'

labels=np.zeros((10),dtype=np.int16)
curpos=0

flbl=open(f77f+".lbif","w")
with open(f77f,"r") as foldf:
    line = foldf.readline()
    while line:
        tline=line.rstrip()
        if is_a_newif(tline):
            if curpos==0:
                labels[0]=100
            else:
                labels[curpos]=newIF(labels[curpos-1])
            tline=tline+" :IL"+str(labels[curpos])
            curpos=curpos+1
        elif is_endif(tline):
            tline=tline+" :IL"+str(labels[curpos-1])
            curpos=curpos-1
        flbl.write(tline+'\n')
        line = foldf.readline()

flbl.close()
print("please check file %s"%(f77f+".lbif"))
