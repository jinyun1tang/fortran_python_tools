import time

def is_comment(tline):
    """
    is a comment line
    """
    return tline[0].upper()=='C'
def is_boolexp(tline):
    """
    determine if it is a bool expression
    """

    return '.LT.' in tline \
    or '.GT.' in tline \
    or '.EQ.' in tline \
    or '.GE.' in tline \
    or '.LE.' in tline \
    or '.AND.' in tline \
    or '.OR.' in tline \
    or '.NE.' in tline

def is_openfl(tline):
    """
    is an open statement
    """
    return tline[0:5]=='OPEN('

def is_continue(tline):
    """
    is a coninuing line
    """

    return  ord(tline[5])>ord(' ')

def is_special(tline):

    if 'CALL ' in tline[0:5]:
        return True
    if 'CHARACTER' in tline:
        return True
    if 'CONTAINS' in tline:
        return True
    if 'CONTINUE' in tline:
        return True
    if 'DATA' in tline[0:4]:
        return True
    if 'DIMENSION' in tline:
        return True
    if 'ENDIF' in tline:
        return True
    if 'END ' in tline[0:5]:
        return True
    if 'ELSE' in tline and not 'ELSEIF' in tline:
        return True
    if 'FORMAT' in tline:
        return True
    if 'FUNCTION' in tline:
        return True
    if 'GO TO' == tline[0:5]:
        return True
    if 'LOGICAL' in tline:
        return True
    if 'include' in tline:
        return True
    if 'INTEGER' in tline:
        return True
    if 'PARAMETER' in tline:
        return True
    if 'PAUSE' in tline:
        return True
    if 'PRIVATE' == tline[0:7]:
        return True
    if 'PRINT' in tline:
        return True
    if 'PROGRAM' in tline:
        return True
    if 'PUBLIC' == tline[0:6]:
        return True
    if 'READ' in tline:
        return True
    if 'REAL*' in tline:
        return True
    if 'RETURN' in tline:
        return True
    if 'STOP' in tline:
        return True
    if 'SUBROUTINE' in tline:
        return True
    if 'WRITE' in tline:
        return True
    if '::' in tline:
        return True

def is_ifthenstruct(tline):
    """
    is an if () then structure
    """
    return 'IF' in tline and 'THEN' in tline
def is_ifstruct(line):
    """
    is an if () do sth structure
    """
    tline=cstrip(line)
    return 'IF(' ==tline[0:3] and not 'THEN' in tline

def is_dostruct(tline):
    """
    is a do statement
    """
    return 'DO ' == tline[0:3]

def get_dostem(line):
    """
    extract the "N=beg, end" part from the do statement
    """
    sl=line[3:].strip()
    nl=len(sl)
    for jl in range(0,nl):
        if (ord(sl[jl])-ord('9')) >0 or (ord(sl[jl])-ord('0')) < 0:
            break
    return sl[jl:].strip()

def extrat_ifthen(line):
    """
    the line is like (ELSE)IF (...) then
    extract the content in (...)
    """
    nel=len(line)
    for j1 in range(nel):
        if line[j1] == '(':
            break
    for j2 in range(nel):
        if line[nel-1-j2] ==')':
            break
    return line[j1+1:(nel-1-j2)]

def extract_if(line):
    """
    the line is like if()expr
    extract contents in () and expr
    """
    nel=len(line)
    for j1 in range(nel):
        if line[j1] == '(':
            break
    j2=0
    for j in range(j1,nel):
        if line[j] == '(':
            j2=j2+1
        elif line[j] ==')':
            j2=j2-1
        if j2 == 0 and line[j] == ')':
            break
    stem=line[j1+1:j]
    tail=line[j+1:]
    if 'GO TO' in tail:
        tail=''
    return stem,tail

def rm_label(line):
    j=-1
    for x in line:
        if x >='0' and x <= '9':
            j=j+1
        else:
            break
    if j==-1:
        label=''
        line1=line.strip()
    else:
        label=line[0:j]
        line1=line[j+1:].strip()
    return label,line1


def rm_arr_indexl(line):
    """
    remove index of arrays
    """

    line1=''
    start=False
    ostart=False
    j=0
    nl=len(line)
    for jl in range(nl):
        x=line[jl]
        if x==':' and line[jl-1] == ':':
            ostart=True
        if ostart:
            if start:
                if x == ',':
                    line1=line1+':,'
                elif x==')':
                    start=False
                    line1=line1+':'+x
            else:
                if x == '(':
                    start=True
                line1=line1+x
        else:
            line1=line1+x
    return line1.strip()


def hline_break(line):
    nl=len(line)
#    head=''
#    stem=''
    for jj in range(nl):
        if line[jj:jj+2]=='::':
            head=line[0:jj]
            stem=line[jj+2:]
            break
    return head,stem;

def var_list():

    varl=[]
    for j in range(26):
        varl.append([])
    return varl;

def stem_break(stem):
    """
    break stem into
    """
    ll=len(stem.strip())
    j0=0
    slist=[]
    for j in range(1,ll):
        if isalnum(stem[j-1]) and stem[j] == ',':
            s=stem[j0:j]
            if '=' in s:
                x=s.split('=')
                slist.append(x[0].strip())
            else:
                slist.append(s.strip())
            j0=j+1
        elif stem[j-1] == ')' and stem[j] == ',':
            s=stem[j0:j]
            slist.append(s.strip())
            j0=j+1
    s=stem[j0:]
    if '=' in s:
        x=s.split('=')
        slist.append(x[0].strip())
    else:
#        print('sl')
#        print(slist)
#        print(s)
        slist.append(s.strip())
#    print(stem)
#    print(slist)
    return slist

def isalnum(c):

    if c>='0' and c <='9':
        return True
    if c>='a' and c <= 'z':
        return True
    if c>='A' and c <= 'Z':
        return True

    return False

def add_varlist(varl,slist):
    """
    add variable slist to varl
    """
    nl=len(slist)
    print('nl')
    print(nl)
    for j in range(nl):
        print('slistx: '+slist[j])
        print(slist[j]())

def get_include_files(hl,hlfs):
    """
    get head file from include line
    """
    hls=[]
    for line in hl:
        x=line.split(" ")
        s=""
        for y in x[1]:
            if y != '"':
                s=s+y
        for x in hlfs:
            if s in x:
                hls.append(x)
    return hls

def rm_arr_indexs(ss):

    s=cstrip(ss)
    if ')(' in s:
        nl = len(s)
        for j in range(nl):
            if s[j:j+2]==')(':
                s=s[0:j+1]
    nl=len(s)
    start=False
    s1=''
    for jl in range(nl):
        if not start:
            s1=s1+s[jl]
        if s[jl] == '(':
            start=True
            continue
        if start:
            if s[jl] == ',':
                s1=s1+':,'
            elif s[jl] == ')':
                s1=s1+':)'
    return s1

def break_boolexp(stem):
    """
    break down ifstem structure e.g.
    VLPO4(L,NY,NX).GT.ZERO.AND.CH2P4(L,NY,NX).GT.UPMNPO(N,NZ,NY,NX)
    into
    VLPO4(L,NY,NX),ZERO.AND.CH2P4(L,NY,NX).GT.UPMNPO(N,NZ,NY,NX)

    """
    nl=len(stem)
    j0=0
    vlst=[]
    for jl in range(j0,nl):
        if stem[jl]=='.' and jl+4 < nl:
            if is_digit(stem[j0:jl+2]):
                #this '.' is part of a number, so keep searching,
                continue
#            if is_digit(stem[j0:jl+1])
            if stem[jl:jl+4] == '.NE.' or \
                stem[jl:jl+4] == '.EQ.' or \
                stem[jl:jl+4] == '.GE.' or \
                stem[jl:jl+4] == '.LE.' or \
                stem[jl:jl+4] == '.GT.' or \
                stem[jl:jl+4] == '.LT.' or \
                stem[jl:jl+4] == '.OR.':
                s=stem[j0:jl]
                vlst.append(s)
                j0=jl+4
                break
            elif jl+5<nl:
                if stem[jl:jl+5] == '.AND.':
                    s=stem[j0:jl]
                    vlst.append(s)
                    j0=jl+5
                break

    if j0 < nl:
        s=stem[j0:]
        vlst.append(s)
    return vlst

def break_dostruct(stem):
    """
    break down the first line of a do statement
    """
    vlst=[]
    x=stem.split('=')
    vlst.append(x[0])
    ss=cstrip(x[1])
#    print('break do 1')
    changed,vlst1=break_dostem(ss,first_do=True)
#    print('sss='+ss)
#    print(vlst1)
    ss=vlst1.pop()
    for s in vlst1:
        vlst.append(s)
#    print(vlst)
#    print(ss)
#    print('break do 2')
    changed,vlst1=break_dostem(ss,first_do=False)
#    print(vlst1)
    if changed:
        for s in vlst1:
            if not is_digit(s):
                vlst.append(s)
    else:
        vlst.append(ss)
    return vlst

def break_dostem(s,first_do):
    """
    break down do stem, e.g.
    M=a,b
    """
#    print('breakdo')
#    print('s====='+s)
    changed=False
    vlst=[]

    nl=len(s)
    for j in range(nl):
        if s[j] =='(' and ',' not in s[0:j]:
            #a is an array or function
            #the statement is of the format N(),M or N(),M,M1
            j0=1
            for k in range(j+1,nl):
                if s[k] =='(':
                    j0=j0+1
                elif s[k] == ')':
                    j0=j0-1
                if s[k]==',' and j0==0:
                    #extra & analyze a
                    vsllh,vsll=break_exprl(s[0:k])
                    for ss in vsll:
                        vlst.append(ss)
                    changed=True
                    break
            break
        elif s[j] ==',' and '(' not in s[0:j]:
            #a is not an array or function
            #extrac a
            #the statement is of the format N,N(),M1
            vlst.append(s[0:j])
            k=j
            changed=True
#            print('here')
#            print(s[j:])
            break
#    print(changed)
#    print(s)
#    print('vlstttt')
#    print(vlst)
    if vlst:
        s1=vlst.pop()
        if algo_operator_in(s1):
            vsllh,vsll=break_exprl(s1)
            for ss in vsll:
                vlst.append(ss)
        else:
            vlst.append(s1)

    if changed:
#        print(s[k+1:])
        if first_do:
            vlst.append(s[k+1:])
        else:
    #extra & analyze b
            vsllh,vsll=break_exprl(s[k+1:])
#            print(vsll)
            for ss in vsll:
                vlst.append(ss)
#    print(vlst)
    if not vlst:
#        if algo_operator_in(s):
        vsllh,vsll=break_exprl(s)
        for ss in vsll:
            vlst.append(ss)
            changed=True

    for ss in vlst:
        if is_digit(ss):
            vlst.remove(ss)
    return changed,vlst

def algo_operator_in(s):
    """
    check if there is algebraic operator in s
    """
    return '+' in s or \
        '-' in s or \
        '*' in s or \
        '/' in s
def is_digit(s):
    """
    determine if a given string is a number
    """
    s1=s
    if 'E' in s1:
        #number represented in E form
        if s1[0] == 'E':
            return False
        y=s1.split('E')
        s2=y[0]

        for x in s2:
            if (ord(x) < ord('0') or ord(x) > ord('9')) \
                and (x != '.') and (x != '-'):
                return False
        s2=y[1]
        for x in s2:
            if (ord(x) < ord('0') or ord(x) > ord('9')) \
                and (x != '.') and (x != '-') and (x != '+'):
                return False
        return True
    else:
        for x in s:
            if (ord(x) < ord('0') or ord(x) > ord('9')) \
                and (x != '.') and (x != '-'):
                return False
        return True

def is_algo_operator(c):
    return c=='*' or c=='+' or c =='-' or c== '/' or c=='**'

def is_bool_operator(c):
    return c=='.NE.' or c=='.EQ.' or c=='.LE.' or c=='.LT.' \
        or c=='.GT.' or c=='.GE.' or c=='.OR.' or c=='.AND.'

def break_expr(ss1):
    """
    break down a regular expression
    """
    vlst=[]
    found_op=False
    #remove any leading operator
    if is_algo_operator(ss1[0]):
        ss=ss1[1:]
        found_op=True
    elif is_bool_operator(ss1[0:4]):
        ss=ss1[4:]
        found_op=True
    elif is_bool_operator(ss1[0:5]):
        ss=ss1[5:]
        found_op=True
    else:
        ss=ss1
    if found_op:
        return found_op,[ss]
#    print('ssssss1')
#    print(ss)
    nl=len(ss)
    for j in range(nl):
        if is_algo_operator(ss[j]):
            j1=j+1
            break
        if j+2 < nl and is_algo_operator(ss[j:j+2]):
            j1=j+2
            break
        if j+4 < nl and is_bool_operator(ss[j:j+4]):
            j1=j+4
            break
        if j+5 < nl and is_bool_operator(ss[j:j+5]):
            j1=j+5
            break
    if j < nl-1:
        if j==0:
            """
            this implies '+' or '-'
            """
            vlst.append(ss[1:])
        else:
            vlst.append(ss[0:j])
            vlst.append(ss[j1:])
    else:
        vlst.append(ss)
    return found_op,vlst

def brace_break(s1):
    """
    break s into multiple strings based on braces
    """
    changed=False
    mult=False
    s=cstrip(s1)
    nl = len(s)
    j0=1
    j1=0
    if s[0] == '(':
        j1=1
        changed=True
    elif s[0] == '.':
        if is_bool_operator(s[0:4]):
            j1=4
            changed=True
            return [s[4:]],changed
        elif is_bool_operator(s[0:5]):
            j1=5
            changed=True
            return [s[5:]],changed
    elif s[0:4] == 'SIN(':
        j1=4
        changed=True
    elif s[0:4] == 'COS(':
        j1=4
        changed=True
    elif s[0:5] == 'ACOS(':
        j1=5
        changed=True
    elif s[0:5] == 'ASIN(':
        j1=5
        changed=True
    elif s[0:4] == 'LOG(':
        j1=4
        changed=True
    elif s[0:4] == 'MOD(':
        j1=4
        mult=True
        changed=True
    elif s[0:4] == 'EXP(':
        j1=4
        if is_algo_operator(s[4]):
            j1=5
        changed=True
    elif s[0:4] == 'INT(':
        j1=4
        changed=True
    elif s[0:4] == 'ABS(':
        j1=4
        changed=True
    elif s[0:4] == 'MAX(':
        j1=4
        mult=True
        changed=True
    elif s[0:4] == 'MIN(':
        j1=4
        mult=True
        changed=True
    elif s[0:5] == 'REAL(':
        j1=5
        changed=True
    elif s[0:5] == 'SQRT(':
        j1=5
        changed=True
    elif s[0:6] == 'AMAX1(':
        changed=True
        mult=True
        j1 = 6
    elif s[0:6] == 'AMIN1(':
        changed=True
        mult=True
        j1=6
    elif s[0:6] == 'CLOSE(':
        changed=True
        j1=6
    else:
        if ':' in s:
            return [s],changed

        for j in range(nl):
            if s[j] =='(' and is_letternums(s[0:j]):
                j1=j+1
                changed=True
                break
        if j>=nl-1:
            return [s],changed
#        print('j1=%d,nl=%d'%(j1,nl))
#        print(s)
#        time.sleep(1)

        #it is an array, this could also be a function
#        for j in range(nl):
#            if s[j]== '(':
#                j1=j+1
#                break
        ss=[]
        j2=j1
        s0=s[0:j1]
        j0=1
        for j in range(j1,nl):
            if s[j] == '(':
                j0=j0+1
            elif s[j] == ')':
                j0=j0-1
            if s[j] ==',' and j0==1:
                ss.append(s[j2:j])
                s0=s0+':,'
                j2=j+1
            elif s[j] ==')' and j0==0:
                s0=s0+':)'
#                print('s0='+s0)
#                print('s2='+s[j2:j])
                ss.append(s[j2:j])
                ss.append(s0)
                break
        if j<nl-1:
            if is_algo_operator(s[j+1]):
                ss.append(s[j+2:])
            else:
                ss.append(s[j+1:])
        changed=True
        return ss,changed
#    else:
#        print('nothing')
#        print(s)
#        return [s],changed

    ss=[]
    j2=j1
#    print(mult)
    for j in range(j1,nl):
        if s[j] == '(':
            j0=j0+1
        elif s[j] == ')':
            j0=j0-1

        if mult:
            #look for
            if s[j] ==',' and j0==1:
                s1=s[j2:j]
                ss.append(s1)
                j2=j+1
            elif s[j] ==')' and j0==0:
                s1=s[j2:j]
                ss.append(s1)
                j2=j+1
                break
        else:
            if s[j] == ')' and j0==0:
                s1=s[j2:j]
                ss.append(s1)
                j2=j+1
                break
    if j < nl-1:
#        print('next')
#        print(s[j+1:])
        if s[j+1] =='.':
            """
            it is a logical expression
            """
            if s[j+4] == '.':
                s2=s[j+5:]
            elif s[j+5]=='.':
                #it is an .and.
                s2=s[j+6:]
#            print('s2='+s2)
        else:
            s2=s[j+2:]
#        print('s2: '+s2)
        ss.append(s2)
    elif j2<nl-1:
        s1=s[j2:nl]
#        print('s1: '+s1)
        ss.append(s1)
#    print(ss)
    return ss,changed


def assign_break(ss):
    """
    break down the string according to '='
    """
    if '=' in ss:
        x=ss.split('=')
        if is_algo_operator(x[1][0]):
            return True,[x[0],x[1][1:]]
        else:
            return True,[x[0],x[1]]
    else:
        return False,[ss]



def break_exprl(line):
    """
    break down a fortran regular expression line
    """
    s=line
    lhs_found,vsl=assign_break(s)
#    print('vslf')
#    print(vsl)
    s1=vsl.pop()
    vlst_lhs=''
    vsl1=[]
    if lhs_found:
#        print(vsl[0])
        vlst_lh=break_expr0(vsl[0])
        vlst_lhs=vlst_lh[0]
        for ss in vlst_lh:
            vsl1.append(ss)
    vlst0=[]
#    print('lhs_found')
#    print(lhs_found)
#    print(vsl1)
#    print('s1ssssss')
#    print(s1)
    vsl=break_expr0(s1)
#    print(vsl)
    for ss in vsl:
        if not ss in vsl1:
            vsl1.append(ss)
#collect the results
#    print('final')
#    print(vsl1)
    return vlst_lhs,vsl1


def break_expr0(s1):

    vlst0=[]
    vsl=[]
    vsl1=[]
    while s1:
#        print('s1xxxx')
#        print(s1)
        vlst1,changed=brace_break(s1)
#        print(changed)
#        print(vlst1)
        if changed:
            for ss in vlst1:
                vlst0.append(ss)
        else:
            #not changed,go through the regular expression breakdown
            s1=vlst1.pop()
#            print('s11111111')
#            print(s1)
            found_op,vlst1=break_expr(s1)
#            print('vlst1111111')
#            print(vlst1)
#            print(found_op)
            if found_op:
                s2=vlst1.pop()
                vlst0.append(s2)
            else:
                if len(vlst1) == 2:
                    s2=vlst1.pop()
                    vlst0.append(s2)

                s2=vlst1.pop()
                vsl.append(s2)
        if vlst0:
            s1=vlst0.pop()
        else:
            s1=''

    for s in vsl:
#        print('fss')
#        print(s)
        if not is_digit(s):
            if '(' in s:
#                print(s)
                s=rm_arr_indexs(s)
#                print('srm')
#                print(s)
            if not s in vsl1:
                vsl1.append(s)
    return vsl1
def break_boolexpl(tline):
    """
    break down a fortran bool expression line
    """
    s1=tline
    vlst0=[]
    vsl=[]
    while s1:
#        print('s1='+s1)
        vlst1,changed=brace_break(s1)
#        print('vlst1')
#        print(changed)
#        print(vlst1)
        if changed:
            for ss in vlst1:
#                print('ss='+ss)
                vlst0.append(ss)
        else:
            #not changed,go through the regular expression breakdown
            vlst1=break_boolexp(s1)
            if len(vlst1) ==2:
                s2=vlst1.pop()
                vlst0.append(s2)
            s2=vlst1.pop()
            vsl.append(s2)
        if vlst0:
            s1=vlst0.pop()
            while True:
                if is_digit(s1):
                    s1=''
                    if vlst0:
                        s1=vlst0.pop()
                        break
                    else:
                        break
                else:
                    break
        else:
            s1=''
    vsl1=[]
    for s in vsl:
        if is_algebra(s):
            vsllh,vsll=break_exprl(s)
            for sl in vsll:
                if not sl in vsl1:
                    vsl1.append(sl)
            continue
        if not is_digit(s):
            if '(' in s:
                s=rm_arr_indexs(s)
            if not s in vsl1:
                vsl1.append(s)
    return vsl1


def is_algebra(s):
    """
    determine if s is an algebraic expression
    """
    return '*' in s \
        or '/' in s \
        or '+' in s \
        or '-' in s



def var_break(line):
    #break a fortran line into a list of variables
    vsl_lhs=''
    if is_openfl(line):
        vsl=break_openfl(line)
    elif is_ifthenstruct(line):
        """
        statement like IF ... THEN
        """
        stem=extrat_ifthen(line)
#        vsl=break_boolexpl(stem)
#        print(stem)
        tlhs,vsl=break_exprl(stem)
#        print(vsl)
    elif is_ifstruct(line):
        """
        statement like IF .... xx
        """
        stem,tail=extract_if(line)
#        vsl=break_boolexpl(stem)
        tlhs,vsl=break_exprl(stem)
        if tail:
#            print('tail='+tail)
#            print(line)
            vsl_lhs,vlst2=break_exprl(tail)
            if vlst2:
                for ss in vlst2:
                    vsl.append(ss)
    elif is_dostruct(line):
        """
        statement like "DO lbl N=a,b,c"
        with c being optional
        """
        stem=get_dostem(line)
        vsl=break_dostruct(stem)
    else:
        """
        regular expression
        """
        jeq=0
        for c in line:
            if c=='=':
                jeq=jeq+1
                if jeq>=2:
                    break
        if jeq >= 2:
            #this part handel juxtaposition of parameter declarations in the
            #form as: real, parameter :: a=9., c=a*3.0
            x=line.split('=')
            vsl=[]
            for s in x:
#                print(s)
                vsl_lhs1,vsl1=break_exprl(s)
#                print(vsl1)
                for c in vsl1:
                    if ',' in c and '(' not in c:
                        #',' is in array
                        xx=c.split(',')
                        for c1 in xx:
                            if not is_digit(c1):
                                if c1 not in vsl  and c1 !=':':
                                    vsl.append(c1)
                    else:
                        if c not in vsl and c !=':':
                            vsl.append(c)

        else:
            vsl_lhs,vsl=break_exprl(line)
#        print(vsl_lhs)
#        print(vsl)
    for s in vsl:
        if is_digit(s) or "'" in s:
            vsl.remove(s)

    nl = len(vsl)
    for jj in range(nl):
        vsl[jj]=vsl[jj].strip()
    if vsl_lhs:
        vsl_lhs=vsl_lhs.strip()
    return vsl_lhs,vsl


def break_openfl(line):
    """
    extract variable from the open file line
    """
    ss=''
    for c in line:
        if c ==',':
            break
        else:
            ss=ss+c
    sl=[]
    if not is_digit(ss[5:]):
        sl.append(ss[5:])

    return sl


def cstrip(line):
    """
    remove any blanks in line
    """
    s=''
    for c in line:
        if not c == ' ':
            s=s+c
    return s

def is_letternums(s):
    """
    check if the whole string is made up by letters and numbers
    """
    for c in s:
        c1=c.upper()
        if (ord(c1)>ord('Z') or ord(c1)<ord('A')) and \
            (ord(c1)>ord('9') or ord(c1)<ord('0')):
            return False
    return True

def is_letternumc(c):
    """
    check if the whole string is made up by letters and numbers
    """
    c1=c.upper()
    return (ord(c1)<=ord('Z') and ord(c1)>=ord('A')) or \
            (ord(c1)<=ord('9') or ord(c1)>=ord('0'))

def check_pattern(a,b):
    """
    check if a and b has same patterns
    the pattern is given as xxsxxsxsx
    where x means letter or number, s means other symbol that a and b
    are required to have at the same location
    """
    if len(a) != len(b):
        return False

    nl=len(a)
    for j in range(nl):
        if is_letternumc(a[j]):
            if not is_letternumc(b[j]):
                return False
        else:
            if a[j] != b[j]:
                return False
    return True


def decal_break(line):
    """
    break down declaration lines
    """
    nl=len(line)
    j0=0
    lb0=0
    vsl=[]
    slist=[]
    for jj in range(nl):
        if line[jj]=='(' and is_letternumc(line[jj]):
            lb0=lb0+1
        elif line[jj] ==')':
            lb0=lb0-1
        elif line[jj] ==',':
            if lb0==0:
                s=line[j0:jj]
                j0=jj+1
                vsl.append(s)
    vsl.append(line[j0:])
#    print(vsl)
    for s in vsl:
        vsl_lhs,vsl1=var_break(s)

        for ss in vsl1:
            if ss not in slist:
                slist.append(ss)
    return slist


def get_procedure_name(line):
    """
    get name of the subroutine or function
    """
    x=line.split(' ')

    ss=x[1].strip()

    nl=len(ss)
    name=''
    for jj in range(nl):
        if ss[jj] =='(':
            name=ss[0:jj]
            break
    if not name:
        name=ss
    return x[0],name


def get_file_path(file_long):
    """
    get file path of file_long
    """
    nl=len(file_long)
    kk=0
    for jj in range(nl):
        if file_long[nl-1-jj]=='/':
            kk=nl-jj
            break
    return file_long[0:kk]

def get_file_name(file_long):
    """
    get file path of file_long
    """
    nl=len(file_long)
    kk=0
    for jj in range(nl):
        if file_long[nl-1-jj]=='/':
            kk=nl-jj
            break
    return file_long[kk:]
