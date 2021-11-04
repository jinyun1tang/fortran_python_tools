
import numpy as np
import argparse
import sys
from shutil import copyfile

#
# globals

def is_comment(tline):
   return tline[0]=='C'


def newIF(label):

    return label+10

def found_then(line):
    tline=line.upper()
    return (tline.find('THEN')>=6)

def found_endif(line):
    tline=line.upper()
    return (tline.find('ENDIF')>=6)


parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument('--ff77', dest="fold", type=str, nargs=1, default=[""],
  help='the fortran 77 file to be labeled')

args = parser.parse_args()

f77f=args.fold[0]

copyfile(f77f, f77f+".bak")

f77lb=f77f+'.lbif'

labels=np.zeros((30),dtype=np.int16)
curpos=0

flbl=open(f77f+".lbif","w")
lelif=False
with open(f77f,"r") as foldf:
    line = foldf.readline()
    while line:
        tline=line.rstrip()
        #do nothing to comment lines
        if not is_comment(line):
            if tline[6:12].upper()=="ELSEIF":
                lelif=not found_then(tline)
            else:
                if found_then(tline):
                    if not lelif:
                        if curpos==0:
                            labels[0]=100
                        else:
                            labels[curpos]=newIF(labels[curpos-1])
                        tline=tline+" :IL"+str(labels[curpos])+"b"
                        curpos=curpos+1
                    lelif=False
                elif found_endif(tline):
                    tline=tline+" :IL"+str(labels[curpos-1])+"e"
                    curpos=curpos-1

        flbl.write(tline+'\n')
        line = foldf.readline()

flbl.close()
print("please check file %s"%(f77f+".lbif"))
