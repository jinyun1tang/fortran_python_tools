#
import varlibs as vl
import time


sl=["DO 8870 NR=1,NRT(NZ,NY,NX)",
"DO 235 L=NUI(NY,NX),NU(NY,NX)-1",
"DTBLX(NY,NX)=DTBLZ(NY,NX)+CDPTH(NU(NY,NX)-1,NY,NX)",
"IF(DATA(6)(1,1:4).EQ.'auto')THEN",
'DO 125 NN=1,100',
'DO 9845 K=25,0,-1',
'DO 5115 LL=L,NG(NZ,NY,NX)+1,-1',
'FHVSTK(K)=AMAX1(0.0,AMIN1(1.0,(1.0-(1.0-AMAX1(0.0,WGLFG)/WGLF(K,NB,NZ,NY,NX))*EHVST(1,2,NZ,I,NY,NX)/EHVST(1,1,NZ,I,NY,NX))))',
'IF(WGLF(K,NB,NZ,NY,NX).GT.ZEROP(NZ,NY,NX).AND.EHVST(1,1,NZ,I,NY,NX).GT.0.0)THEN',
'FHVST=AMAX1(0.0,1.0-(1.0-FHGT)*EHVST(1,1,NZ,I,NY,NX))',
'DO 9970 LL=NUX+1,NL(NY,NX)',
'PSISM1(NUM(NY,NX),NY,NX)=-EXP(PSIMS(NY,NX)+(((PSL(NUM(NY,NX),NY,NX)-LOG(THETW1))/PSD(NUM(NY,NX),NY,NX))**SRP(NUM(NY,NX),NY,NX)*PSISD(NY,NX)))',
'FLWL(3,NUM(NY,NX),NY,NX)=FLWLW+FLWLG',
'IF(L.EQ.NU(NY,NX).OR.CDPTH(L-1,NY,NX).LT.DPNO3(NY,NX))THEN',
'DO 600 L=JC(N),N1,N2(1,2)',
'IF((IDAY(1,NB1(NZ,NY,NX),NZ,NY,NX).NE.0).AND.(ARLFS(NZ,NY,NX).GT.ZEROL(NZ,NY,NX).AND.FRADP(NZ,NY,NX).GT.0.0).AND.(RTDP1(1,1,NZ,NY,NX).GT.SDPTH(NZ,NY,NX)+CDPTHZ(0,NY,NX)))THEN',
'FPC=ARLFS(NZ,NY,NX)/ARLSS(NY,NX)*AMIN1(1.0,0.5*ARLFC(NY,NX)/AREA(3,NU(NY,NX),NY,NX))',
    'IF(ABS(TKCY-TKC1).LT.0.05*10*(NN/10)*10.EQ.NN)THEN',
    'ELSEIF(EX.LE.0.03.AND.VOLWC(NZ,NY,NX).GT.0.0)THEN',
    'DO 2005 NR=NU1(NU(3)),NRT(NZ,NY,NX)',
    'NN=TEST_CONVERGENCE(TKCX, VHCPX, WVPLT, HFLWC1, PSILH, FPC,MXN,DIFF,UPRT,VFLXC)',
    'DIFFL=POSGX*RTARR(N,L)/LOG(PATHL/RRADL(N,L))',
    'TKG(NZ,NY,NX)=TKS(NU(NY,NX),NY,NX)',
    'RTKNO3=(-B-SQRT(B*B-4.0*C))/2.0',
    'RACZ(NZ,NY,NX)=AMIN1(RACX,AMAX1(0.0,ZT(NY,NX)*EXP(ALFZ)/(ALFZ/RAB(NY,NX))*(EXP(-ALFZ*ZC(NZ,NY,NX)/ZT(NY,NX))-EXP(-ALFZ*(ZD(NY,NX)+ZR(NY,NX))/ZT(NY,NX)))))',
    'RCA=-RPCACX-RPCASO-RXCA-RCAO-RCAC-RCAH-RCAS-(RPCADX+RPCAMX+RC0P+RC1P+RC2P)*VLPO4(L,NY,NX)-(RPCDBX+RPCMBX+RC0B+RC1B+RC2B)*VLPOB(L,NY,NX)-5.0*(RPCAHX*VLPO4(L,NY,NX)+RPCHBX*VLPOB(L,NY,NX))',
    'KL=MAX(1,MIN(100,INT(100.0*(POROS(N6,N5,N4)))))',
    'SSINN(NY,NX)=AMAX1(0.0,AZI+DEC*COS(.2618*(ZNOON(NY,NX)-(J+0.5))))',
    'FINHL(N3,N2,N1)=AMIN1(0.0,AMAX1(FINHX,-VOLPH1X,-VOLW1X))',
    '(J-(ZNOON(NY,NX)-DYLN(NY,NX)/2.0))*3.1416/DYLN(NY,NX)',
    'RUPHGS(N,L,NZ,NY,NX)=RUPHGS(N,L,NZ,NY,NX)+RUPHGX',
    'RHGDF1=AMAX1(-H2GPX,DFGP*(AMAX1(ZEROP(NZ,NY,NX),H2GA1)*VOLWH2-H2GPX*RTVLP(N,L,NZ,NY,NX))/(VOLWH2+RTVLP(N,L,NZ,NY,NX)))',
    'DO 9985 L=NU(NY,NX),NL(NY,NX)',
    'IF(10*B.LT.A.AND.C.GT.E)THEN',
    'IF((I/10)*10.EQ.I.AND.J.EQ.15)THEN',
    'IF(VLPO4(L,NY,NX).GT.ZERO.AND.CH2P4(L,NY,NX).GT.UPMNPO(N,NZ,NY,NX))THEN',
    'IF(SSIN(NY,NX).GT.0.0)TRAD(NY,NX)=TRAD(NY,NX)+RADS(NY,NX)',
    'ELSEIF(THETWX(N3,N2,N1).LT.POROS(N3,N2,N1)-DTHETW)THEN',
    'XP=REAL(IDAY0(NZ,NY,NX))',
    'IF((NN.GE.30.AND.ABS(DPSI).LT.1.0E-03).OR.NN.GE.MXN)GO TO 4250',
    "OPEN(LUN,FILE=trim(prefix)//'years',STATUS='OLD')"]
#first break
real_list_loc=[]
int_list_loc=[]
char_list_loc=[]
bool_list_loc=[]
for j in range(26):
        real_list_loc.append([])
        int_list_loc.append([])
        char_list_loc.append([])
        bool_list_loc.append([])

for line in sl[0:1]:
    line0=line.strip()
    print('Input:')
    print(line0)
    vsl_lhs,vsl=vl.var_break(line0)
    if vsl_lhs:
        print('lhs: '+vsl_lhs)
    for ss in vsl:
        loc=ord(ss[0])-ord('A')
        if (ord(ss[0])-ord('I'))>=0 and (ord(ss[0])-ord('N'))<=0:
            if not ss in int_list_loc[loc]:
                int_list_loc[loc].append(ss)
        else:
            if not ss in real_list_loc[loc]:
                real_list_loc[loc].append(ss)
print('INTEGER:')
print(int_list_loc)
print('REAL:')
print(real_list_loc)
