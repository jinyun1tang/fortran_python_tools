# fortran_python_tools

Tools include

labelifs.py

labels all IF structures.

varAnalyzer.py

reports variable use for subroutine files.

varAnalyzerv2.py

reports variable use for module files.

proceduresplit.py

splits subroutines based on subroutine headers.

insertf77space.py

adds space to conform with f77 format.



hfile.ls contains the list of head files needed by varAnalyzer.py
and varAnalyzerv2.py. It should be updated accordingly.

type

python script_name.py --help

for information.


To use varAnalyzerv2.py, some modifications of the module file is needed.
An example can be found at

https://github.com/jinyun1tang/EcoSIM/blob/jytang/modular/f77src/ecosys_mods/GrosubMod.f

where 'C     include_section', 'C     end_include_section', and 'C     begin_execution'
are added to help identify the proper blocks.

proceduresplit.py carves out subroutines by paired labels like 'C      subroutine subname' and
'C      end subroutine subname' 
