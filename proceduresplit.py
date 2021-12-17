import argparse
import sys
from shutil import copyfile
import os.path
import varlibs as vl
import subprocess

parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument('--ff77', dest="fold", type=str, nargs=1, default=[""],
  help='the fortran 77 file to be labeled')

parser.add_argument('--opr', dest="operation", type=str, nargs=1, default=[""],
  help='type of operation')

args = parser.parse_args()

f77f=args.fold[0]

forb=args.operation[0]

subprocess.run(["mkdir", "-p","work"])

fnm=vl.get_file_name(f77f)
fbak='./work/'+fnm+".bak"

if forb.upper() == 'F':
    print("Do procedure splitting for file "+f77f)
    if os.path.exists(fbak):
        yesno=input('Overwite File '+fbak+'? [yes/no] ')
        if yesno[0].upper()=='Y':
            print('Overwite File '+fbak)
            copyfile(f77f, fbak)
    else:
        copyfile(f77f, fbak)
    subf=[]
    stage=0
    fwr=open(f77f,'w')
    with open(fbak,"r") as foldf:
        line = foldf.readline()
        while line:
            if "C      subroutine"==line[0:17]:
                subf.append(line[1:])
                fwr.write('      call'+line[17:].rstrip()+'\n')
#                print('      call'+line[17:].rstrip()+'\n')
                stage=1
            else:
                if 'C      end subroutine' ==line[0:21]:
                    stage=0
                    subf.append(line[1:])
                elif 'end module ' in line.lower():
                    fwr.write('C'+'-'*90+'\n')
#                    print('C'+'-'*90+'\n')
                    for ss in subf:
                        fwr.write(ss.rstrip()+'\n')
#                        print(ss.rstrip())
                    fwr.write(line.rstrip()+'\n')
#                    print(line)
                else:
#                    print('stage=%d'%stage)
                    if stage>0:
                        subf.append(line.rstrip())
                    else:
                        fwr.write(line.rstrip()+'\n')
#                        print(line.rstrip())

            line = foldf.readline()
    fwr.close()
else:
    print('Revert last procedure splitting')
    copyfile(fbak,f77f)
