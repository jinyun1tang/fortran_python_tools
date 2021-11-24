# fortran_python_tools

Type the following command 

python varAnalyzer.py --help

for how to use varAnalyzer.py to analyze the variable usage of a given f77 file.

One example output is 

wthr.f.var,

which is generated from using 

python varAnalyzer.py --hlist hfile.ls --ff77 ../EcoSIM/f77src/ecosys_src/wthr.f 

hfile.ls contains the list of head files. 

If this repo is put to the same upper directory like EcoSIM, then not much
change is needed to make the code work. 
