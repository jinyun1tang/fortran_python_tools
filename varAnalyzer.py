import numpy as np
import argparse
import sys
from shutil import copyfile
import varlibs as vl
import hreader as hrd
import subprocess

"""
Currently, the analyzer does not work well with logical and character variables,
which may be regarded as either integers or real variables.
"""

def write_var(wfile,varlist,prefix=''):
    """
    write list varlist to wfile
    """
    kk=0
    if varlist:
        s=prefix
        for c in varlist:
            s=s+c
            if len(s)>62:
                wfile.write(s)
                wfile.write('\n')
                s=prefix
            else:
                s=s+','
        if s and len(s) > len(prefix):
            if s[-1]==',':
                s=s[:-1]
            wfile.write(s)
            wfile.write('\n')

parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument('--ff77', dest="fold", type=str, nargs=1, default=[""],
    help='the fortran 77 file to be labeled')
parser.add_argument('--hlist',dest="hlist",type=str,nargs=1,default=[""],
    help='list of header files to be loaded')

args = parser.parse_args()

f77f=args.fold[0]
hlist=args.hlist[0]

#create the list of head files to be loaded
hlfs=[]
subprocess.run(["mkdir -p work"])

with open(hlist,"r") as foldf:
    line = foldf.readline()
    hf= line.strip()
    while (hf):
        hlfs.append(hf)
        line = foldf.readline()
        hf=line.strip()

#real_list,int_list,char_list,bool_list=hrd.load_heads(hl)

#if len(real_list)>0:
#    print('real:')
#    for rl in real_list:
#        print(rl)

#if len(char_list)>0:
#    print('char')
#    for rl in char_list:
#        print(rl)

#if len(int_list)>0:
#    print('int')
#    for rl in int_list:
#        print(rl)

#if len(bool_list)>0:
#    print('bool')
#    for rl in bool_list:
#        print(rl)

real_list_loc_decl=[]
int_list_loc_decl=[]
char_list_loc_decl=[]
bool_list_loc_decl=[]
for j in range(26):
        real_list_loc_decl.append([])
        int_list_loc_decl.append([])
        char_list_loc_decl.append([])
        bool_list_loc_decl.append([])

real_list_loc_use=[]
int_list_loc_use=[]
for j in range(26):
        real_list_loc_use.append([])
        int_list_loc_use.append([])


print("process file "+f77f)
list_intents=[]
list_locdecl=[]
with open(f77f,"r") as foldf:
    line = foldf.readline()
    line0= line.rstrip()
    start=0
    hl=[]
    var_lhst=[]
    while line:
        tline=line.rstrip()
        if "include" in tline:
# store include lines
            start=1
            hl.append(tline.strip())
        else:
            if start==0:
                #read lines before include
                if (len(line.strip())==0) or vl.is_comment(line):
#                   an empty line or comment line
                    line = foldf.readline()
                    continue
                if vl.is_continue(line):
#                   is a continuing line
                    line0=line0+line[6:].strip()
                else:
                    #not a cotinuing line or comment line, last line has finished
                    if 'intent' in line0.lower():
                        line1=vl.rm_arr_indexl(line0)
                        list_intents.append(line1)
                    line0=line.rstrip()
                line = foldf.readline()
                continue

            elif start==1:
                #the intent below is to handel situations that there are
                #subroutines inside a big subroutine
                if 'intent' in line0.lower():
                    line00=line0.upper()
                    line1=vl.rm_arr_indexl(line00)
                    list_intents.append(line1)

                for line1 in list_intents:
                    head,stem=vl.hline_break(line1.upper())
                    slist=vl.stem_break(stem)
                    nl=len(slist)
                    if 'CHARACTER' in head:
                        for jl in range(nl):
                            loc=ord(slist[jl][0])-ord('A')
                            char_list_loc_decl[loc].append(slist[jl])
                    elif 'REAL' in head:
                        for jl in range(nl):
                            loc=ord(slist[jl][0])-ord('A')
                            real_list_loc_decl[loc].append(slist[jl])
                    elif 'LOGICAL' in head:
                        for jl in range(nl):
                            loc=ord(slist[jl][0])-ord('A')
                            bool_list_loc_decl[loc].append(slist[jl])
                    elif 'INTEGER' in head:
                        for jl in range(nl):
                            loc=ord(slist[jl][0])-ord('A')
                            int_list_loc_decl[loc].append(slist[jl])

                #list of head files is created, load them
                hls=vl.get_include_files(hl,hlfs)
                real_list_head,int_list_head,char_list_head,bool_list_head=hrd.load_heads(hls)
                #now it is ready to sort the locally declared variables
                start=2
                if (len(line.strip())==0) or vl.is_comment(line):
                    line0=""
                else:
                    line0=line.rstrip()
                line=foldf.readline()
                continue
        #the the excutation section is read in
        if start == 2:
            if "execution begins here" in tline:
                #turn on execution part
                start=3
                if '::' in line0:
                    line00=line0.upper()
                    if not 'PARAMETER' in line00:
                        line1=vl.rm_arr_indexl(line00)
                    else:
                        line1=line00
                    list_locdecl.append(line1)
                for line1 in list_locdecl:
                    if not '::' in line1:
                        continue
                    head,stem=vl.hline_break(line1)
                    if 'PARAMETER' in line1:
                        var_lhs1,slist=vl.var_break(stem)
                    else:
                        slist=vl.stem_break(stem)
                    nl=len(slist)
                    if 'CHARACTER' in head:
                        for jl in range(nl):
                            loc=ord(slist[jl][0])-ord('A')
                            char_list_loc_decl[loc].append(slist[jl])
#                vl.add_varlist(char_list,slist)
                    elif 'REAL' in head:
                        for jl in range(nl):
                            loc=ord(slist[jl][0])-ord('A')
                            real_list_loc_decl[loc].append(slist[jl])
#            vl.add_varlist(real_list,stem)
                    elif 'LOGICAL' in head:
                        for jl in range(nl):
                            loc=ord(slist[jl][0])-ord('A')
                            bool_list_loc_decl[loc].append(slist[jl])
#            vl.add_varlist(bool_list,stem)
                    elif 'INTEGER' in head:
                        for jl in range(nl):
                            loc=ord(slist[jl][0])-ord('A')
                            int_list_loc_decl[loc].append(slist[jl])
                line = foldf.readline()
                line0=''
                continue
            #declaration
            if (len(line.strip())==0) or vl.is_comment(line):
#               an empty line or comment line
                line = foldf.readline()
                continue
            if vl.is_continue(line):
                line0=line0+line[6:].strip()
            else:
                if line0.strip():
                    line00=line0.upper()
                    #add to the list of locally declared vars
                    line1=vl.rm_arr_indexl(line00)
                    list_locdecl.append(line1)
                line0=line.rstrip()
        elif start == 3:
            if (len(line.strip())==0) or vl.is_comment(line):
#               an empty line or
                line = foldf.readline()
                continue

            if vl.is_continue(line):
                line0=line0+line[6:].strip()
            else:
                #not a continuous line
                if line0.strip():
                    line00=line0.upper().strip()
                #analyze line0
                    label,line1=vl.rm_label(line00)
#            if len(label.strip())>0:
#                print(label)

                    if not vl.is_special(line1):
                        var_lhs,varlist=vl.var_break(line1)

                        if var_lhs:
                            if not var_lhs in var_lhst:
                                var_lhst.append(var_lhs)
                        for ss in varlist:
                            loc=ord(ss[0])-ord('A')
                            if (ord(ss[0])-ord('I'))>=0 and (ord(ss[0])-ord('N'))<=0:
                                if not ss in int_list_loc_use[loc]:
                                    int_list_loc_use[loc].append(ss)
                            else:
                                if not ss in real_list_loc_use[loc]:
                                    real_list_loc_use[loc].append(ss)
                #this a labeled lin
            #get a new line
                line0=line.rstrip()
        #break the line into list variables
        line = foldf.readline()

"""
Identify variables that have not been declared
"""

real_undecl=[]
int_undecl=[]
for jj in range(26):
    for ss in real_list_loc_use[jj]:
        if ss not in real_list_loc_decl[jj] \
            and ss not in real_list_head[jj] \
            and ss not in bool_list_head[jj] \
            and ss not in bool_list_loc_decl[jj] \
            and ss not in char_list_head[jj] \
            and ss not in char_list_loc_decl[jj]:
            real_undecl.append(ss)

    for ss in int_list_loc_use[jj]:
        if ss not in int_list_loc_decl[jj] \
            and ss not in int_list_head[jj] \
            and ss not in bool_list_loc_decl[jj] \
            and ss not in bool_list_head[jj] \
            and ss not in char_list_loc_decl[jj] \
            and ss not in char_list_head[jj]:
            int_undecl.append(ss)

ff=f77f.split('/')
frpt=ff[-1]+'.var'
with open(frpt,"w") as frptf:
    frptf.write('Summary of variables in '+f77f+'\n')
    frptf.write('='*90+'\n')
    frptf.write('Variables not declared\n')
    frptf.write('-'*90+'\n')
    frptf.write('REAL:\n')
    frptf.write('-'*90+'\n')
    write_var(frptf,real_undecl,'      real(r8) :: ')
    frptf.write('-'*90+'\n')
    frptf.write('INTEGER:\n')
    frptf.write('-'*90+'\n')
    write_var(frptf,int_undecl,'      integer :: ')
    frptf.write('='*90+'\n')
    frptf.write('Value changing variables\n')
    write_var(frptf,var_lhst)
    frptf.write('='*90+'\n')
    frptf.write('head files included\n')
    for hf in hlfs:
        frptf.write(hf+'\n')
    frptf.write('='*90+'\n')
#bool_list_head
    frptf.write('Locally declared variables\n')
    frptf.write('-'*90+'\n')
    frptf.write('REAL:\n')
    frptf.write('-'*90+'\n')
    for l in range(26):
        write_var(frptf,real_list_loc_decl[l])
    frptf.write('-'*90+'\n')
    frptf.write('INTEGER:\n')
    frptf.write('-'*90+'\n')
    kk=0
    for l in range(26):
        write_var(frptf,int_list_loc_decl[l])
    frptf.write('-'*90+'\n')
    frptf.write('CHARACTER:\n')
    frptf.write('-'*90+'\n')
    for l in range(26):
        write_var(frptf,char_list_loc_decl[l])
#char_list_decl
    frptf.write('-'*90+'\n')
    frptf.write('LOGICAL:\n')
    frptf.write('-'*90+'\n')
    for l in range(26):
        write_var(frptf,bool_list_loc_decl[l])
#bool_list_decl
    frptf.write('='*90+'\n')
    frptf.write('Variables used in the file\n')
    frptf.write('-'*90+'\n')
    frptf.write('REAL:\n')
    frptf.write('-'*90+'\n')
    for l in range(26):
#        frptf.write(chr(ord('A')+l)+': ')
#        if l == ord('K')-ord('A'):
#            print(real_list_loc_use[l])
        write_var(frptf,real_list_loc_use[l])
#real_list_loc_use
    frptf.write('-'*90+'\n')
    frptf.write('INTEGER:\n')
    frptf.write('-'*90+'\n')
    for l in range(26):
        write_var(frptf,int_list_loc_decl[l])

#int_list_loc_use
