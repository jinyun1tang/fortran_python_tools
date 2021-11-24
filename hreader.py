#def break_if(line):
import argparse
import varlibs as vl

def load_header(headf,real_list,int_list,char_list,bool_list):
    """load header file
    """
    lines=[]
    print(headf)
    start=True
    with open(headf,"r") as foldf:
        line = 'x'
        line0= ''
        while line:
            line = foldf.readline()

            if "COMMON" in line:
                line1=vl.rm_arr_indexl(line0)
                lines.append(line1)
                break
            if len(line.strip())==0 or vl.is_comment(line):
                continue
            if vl.is_continue(line):
                line0=line0+line[6:].strip()
            else:
                #new  line
                if line0:
                    line1=vl.rm_arr_indexl(line0)
#                    print('line1')
#                    print(line1)
#                    print('line')
#                    print(line)
                    lines.append(line1)
#                    start=False
                line0=line.rstrip()
#    print(len(lines))
    if not lines:
        lines.append(line0)
    for line in lines:
#        print(line)
        head,stem=vl.hline_break(line.upper())
#        print('head: '+head)
#        print(stem)
        slist=vl.stem_break(stem.strip())
        nl=len(slist)
        if 'CHARACTER' in head:
            for jl in range(nl):
                loc=ord(slist[jl][0].upper())-ord('A')
                char_list[loc].append(slist[jl])
#                vl.add_varlist(char_list,slist)
        elif 'REAL' in head:
            for jl in range(nl):
                loc=ord(slist[jl][0].upper())-ord('A')
                real_list[loc].append(slist[jl])
#            vl.add_varlist(real_list,stem)
        elif 'LOGICAL' in head:
            for jl in range(nl):
                loc=ord(slist[jl][0].upper())-ord('A')
                bool_list[loc].append(slist[jl])
#            vl.add_varlist(bool_list,stem)
        elif 'INTEGER' in head:
            for jl in range(nl):
                loc=ord(slist[jl][0].upper())-ord('A')
                int_list[loc].append(slist[jl])
#            vl.add_varlist(int_list,stem)
    return real_list,int_list,char_list,bool_list

def load_heads(hflist):
    """
    load variables from the list of header files in hflist
    """
    real_list=[]
    int_list=[]
    char_list=[]
    bool_list=[]
    for j in range(26):
        real_list.append([])
        int_list.append([])
        char_list.append([])
        bool_list.append([])
    #loop through the list of files
    for hf in hflist:
        real_list,int_list,char_list,bool_list=load_header(hf,
            real_list,int_list,char_list,bool_list)

    return real_list,int_list,char_list,bool_list




#parser = argparse.ArgumentParser(description=__doc__)

#parser.add_argument('--hfile_list', dest="fold", type=str, nargs=1, default=[""],
#  help='the list of fortran 77 header files to read')

#args = parser.parse_args()

#f77f=args.fold[0]

#real_list,int_list,char_list,bool_list=load_heads(f77f)

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
