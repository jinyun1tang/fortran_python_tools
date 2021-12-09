import numpy as np
import argparse
import sys
from shutil import copyfile
import varlibs as vl
import hreader as hrd



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
    help='the fortran 77 file to be processed')
parser.add_argument('--hlist',dest="hlist",type=str,nargs=1,default=[""],
    help='list of header files to be loaded')

args = parser.parse_args()

f77f=args.fold[0]
hlist=args.hlist[0]

#create the list of head files to be loaded
hlfs=[]

real_list_mod_decl=[]
int_list_mod_decl=[]
char_list_mod_decl=[]
bool_list_mod_decl=[]
for jj in range(26):
    real_list_mod_decl.append([])
    int_list_mod_decl.append([])
    char_list_mod_decl.append([])
    bool_list_mod_decl.append([])


with open(hlist,"r") as foldf:
    line = foldf.readline()
    hf= line.strip()
    while (hf):
        hlfs.append(hf)
        line = foldf.readline()
        hf=line.strip()

stage=0
sstage=-1
print("process file "+f77f)
hlfs_loc=[]
line3=''

ff=f77f.split('/')
frpt=ff[-1]+'.var'
fwr = open(frpt, "w")
fwr.write('Summary of variables in '+f77f+'\n')
fwr.write('='*90+'\n')
proc_type=''
proc_name=''
with open(f77f,"r") as foldf:
    line = foldf.readline()
    while line:
        line0= line.rstrip().upper()
        line1= line.strip()
        line2= line.strip().upper()
        if stage==0:  
            if "IMPLICIT NONE" in line2:
                stage=1
        elif stage==1:
#            print(line0)
            if "include" == line1[0:7]:
                hlfs_loc.append(line1)
                pass        
            else:
#                print(line0)
                if "end_include_section" in line:
                    """
                    load all included .h files
                    """
#                    print('here')
                    stage=2
                    hls=vl.get_include_files(hlfs_loc,hlfs)
#                    for hl in hls:
#                        print(hl)
                    real_list_head,int_list_head,char_list_head,bool_list_head=hrd.load_heads(hls)
#                    for jj in range(26):
#                        print(real_list_head[jj])
                    line3=''    
        elif stage==2:
            """
            declaration section
            """
#            print(line2)
            if "CONTAINS" == line2[0:8]:
                stage=3
                """
                write globally declared variables
                """
                line3=''
            elif (len(line.strip())==0) or vl.is_comment(line):
                pass
            else:
                if vl.is_continue(line0):
                    line3=line3+line0[6:]
                else:
                    if line3:
                        #break line 
                        if 'DATA' == line3[0:4]:
                            pass
                        elif 'PUBLIC' == line3[0:6]:
                            pass
                        elif 'PRIVATE' == line3[0:7]:
                            pass
                        else:    
                            head,stem=vl.hline_break(line3)
                            slist=vl.decal_break(stem.strip())
                            nl=len(slist)
                            if 'CHARACTER' in head:
                                for jl in range(nl):
                                    loc=ord(slist[jl][0].upper())-ord('A')
                                    if slist[jl] not in char_list_mod_decl[loc]:
                                        char_list_mod_decl[loc].append(slist[jl])
#                vl.add_varlist(char_list,slist)
                            elif 'REAL' in head:
                                for jl in range(nl):
                                    loc=ord(slist[jl][0].upper())-ord('A')
                                    if slist[jl] not in real_list_mod_decl[loc]:
                                        real_list_mod_decl[loc].append(slist[jl])
#            vl.add_varlist(real_list,stem)
                            elif 'LOGICAL' in head:
                                for jl in range(nl):
                                    loc=ord(slist[jl][0].upper())-ord('A')
                                    if slist[jl] not in bool_list_mod_decl[loc]:
                                        bool_list_mod_decl[loc].append(slist[jl])
#            vl.add_varlist(bool_list,stem)
                            elif 'INTEGER' in head:
                                for jl in range(nl):
                                    loc=ord(slist[jl][0].upper())-ord('A')
                                    if slist[jl] not in int_list_mod_decl[loc]:
                                        int_list_mod_decl[loc].append(slist[jl])
                    line3=line2            
                         
        elif stage==3:
            """
            procedures in the module            
            """

            if sstage==0:
                if "IMPLICIT NONE" in line2:
                    """
                    entering variable declartion stage
                    """
                    sstage=1
                    pass
            else:        
                if sstage!=0 and ('SUBROUTINE' == line2[0:10] or 'FUNCTION ' in line2) and not vl.is_comment(line1):
                    """
                    subroutine begin
                    """
                    proc_type,proc_name=vl.get_procedure_name(line2)
                    sstage=0
                    real_list_loc_decl=[]
                    int_list_loc_decl=[]
                    char_list_loc_decl=[]
                    bool_list_loc_decl=[]
                    """
                    unless bool or character variables are marked, the analyzer
                    is not able to recognize them
                    """
                    real_list_loc_used=[]
                    int_list_loc_used=[]
                    real_list_loc_lhs=[]
                    int_list_loc_lhs=[]
                    for jj in range(26):
                        real_list_loc_decl.append([])
                        int_list_loc_decl.append([])
                        char_list_loc_decl.append([])
                        bool_list_loc_decl.append([])     
                    line3=''
                    pass
                elif 'END' == line2[0:3] and ('SUBROUTINE' in line2 or 'FUNCTION' in line2):
                    """
                    end of subroutine
                    summarize variables used in the subroutine, and variables
                    not declared in the subroutine
                    """
                    real_loc_not_decl=[]
                    int_loc_not_decl=[]
                    real_list_loc_const=[]
                    int_list_loc_const=[]

                    for vv in real_list_loc_used:
                        jj=ord(vv[0])-ord('A')                        
                        if vv not in real_list_loc_decl[jj] \
                            and vv not in real_list_head[jj] \
                            and vv not in bool_list_head[jj] \
                            and vv not in bool_list_loc_decl[jj] \
                            and vv not in char_list_head[jj] \
                            and vv not in char_list_loc_decl[jj]:
                                    real_loc_not_decl.append(vv)  #used but not locally declared
                                    
                        if vv not in real_list_loc_lhs:
                            real_list_loc_const.append(vv)    

                    for vv in int_list_loc_used:
                        jj=ord(vv[0])-ord('A')                                                
                        if vv not in int_list_loc_decl[jj] \
                            and vv not in int_list_head[jj] \
                            and vv not in bool_list_head[jj] \
                            and vv not in bool_list_loc_decl[jj] \
                            and vv not in char_list_head[jj] \
                            and vv not in char_list_loc_decl[jj]:
                            int_loc_not_decl.append(vv)  #used but not locally declared
                                
                        if vv not in int_list_loc_lhs:
                            int_list_loc_const.append(vv)
                    """
                    write summary report
                    """                    
                    fwr.write("%s %s\n"%(proc_type,proc_name))
                    fwr.write('='*90+'\n') 
                    fwr.write('Real variables\n')
                    fwr.write('+'*90+'\n')
                    fwr.write('Used\n')
                    fwr.write('-'*90+'\n')
                    write_var(fwr,real_list_loc_used,prefix='real(r8): ')                    
                    fwr.write('-'*90+'\n')
                    fwr.write('Value changing\n')  
                    fwr.write('-'*90+'\n')                    
                    write_var(fwr,real_list_loc_lhs,prefix='real(r8): ')                    
                    fwr.write('-'*90+'\n')
                    fwr.write('Not value changing\n')
                    fwr.write('-'*90+'\n')                    
                    write_var(fwr,real_list_loc_const,prefix='real(r8): ')
                    fwr.write('-'*90+'\n')
                    fwr.write('Not declared locally\n')  
                    fwr.write('-'*90+'\n')
                    write_var(fwr,real_loc_not_decl,prefix='real(r8): ')
                    fwr.write('-'*90+'\n')                    
                    fwr.write('Integer variables\n')
                    fwr.write('+'*90+'\n')
                    fwr.write('Used\n')                    
                    fwr.write('-'*90+'\n')                                        
                    write_var(fwr,int_list_loc_used,prefix='integer: ')  
                    fwr.write('-'*90+'\n')
                    fwr.write('Value changing\n')
                    fwr.write('-'*90+'\n')
                    write_var(fwr,int_list_loc_lhs,prefix='integer: ')  
                    fwr.write('-'*90+'\n')
                    fwr.write('Not value changing\n')  
                    fwr.write('-'*90+'\n')
                    write_var(fwr,int_list_loc_const,prefix='integer: ')  
                    fwr.write('-'*90+'\n')
                    fwr.write('Not declared locally\n')  
                    fwr.write('-'*90+'\n')
                    write_var(fwr,int_loc_not_decl,prefix='integer: ')  
                    fwr.write('='*90+'\n')
                                  
                    pass
                elif sstage == 1:                                         
                    if 'begin_execution' in line1:
                        """
                        end the variable declaration stage
                        """
                        sstage=2
                        line3=''
                        pass 
                    else:
                        """
                        add local variable declaration
                        """
                        if line1:
                            if not vl.is_comment(line1):
                                head,stem=vl.hline_break(line2)
                                slist=vl.decal_break(stem.strip())
                                nl=len(slist)
                                if 'CHARACTER' in head:
                                    for jl in range(nl):
                                        loc=ord(slist[jl][0].upper())-ord('A')
                                        if slist[jl] not in char_list_loc_decl[loc]:
                                            char_list_loc_decl[loc].append(slist[jl])
#                vl.add_varlist(char_list,slist)
                                elif 'REAL' in head:
                                    for jl in range(nl):
                                        loc=ord(slist[jl][0].upper())-ord('A')
                                        if slist[jl] not in real_list_loc_decl[loc]:
                                            real_list_loc_decl[loc].append(slist[jl])
#            vl.add_varlist(real_list,stem)
                                elif 'LOGICAL' in head:
                                    for jl in range(nl):
                                        loc=ord(slist[jl][0].upper())-ord('A')
                                        if slist[jl] not in bool_list_loc_decl[loc]:
                                            bool_list_loc_decl[loc].append(slist[jl])
#            vl.add_varlist(bool_list,stem)
                                elif 'INTEGER' in head:
                                    for jl in range(nl):
                                        loc=ord(slist[jl][0].upper())-ord('A')
                                        if slist[jl] not in int_list_loc_decl[loc]:
                                            int_list_loc_decl[loc].append(slist[jl])
                                
                elif sstage==2:
                    if line1:
                        if vl.is_comment(line0):
                            pass
                        else:
                            if vl.is_continue(line0):
                                line3=line3+line0[6:]
                                pass
                            else:
                                if line3:
                                    var_lhs1,slist=vl.var_break(line3)
                                    vv=var_lhs1
                                    if vv:
                                        if (ord(vv[0])-ord('I'))>=0 and (ord(vv[0])-ord('N'))<=0:
                                            if vv not in int_list_loc_lhs:
                                                int_list_loc_lhs.append(vv)
                                        else:
                                            if vv not in real_list_loc_lhs:
                                                real_list_loc_lhs.append(vv)
                                        
                                    for vv in slist:                                    
                                        if (ord(vv[0])-ord('I'))>=0 and (ord(vv[0])-ord('N'))<=0:
                                            if vv not in int_list_loc_used:
                                                int_list_loc_used.append(vv)
                                        else:
                                            if vv not in real_list_loc_used:
                                                real_list_loc_used.append(vv)

                                line3=line2
                                if vl.is_special(line2):   
                                    line3=''
                                 
        line=foldf.readline()

fwr.close()       
print('Check summary file %s'%frpt)     