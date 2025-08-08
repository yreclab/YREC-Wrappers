# YREC-Wrappers
Wrappers, helpful codes, and additional machinery to interface with YREC with languages such as Python. 

newheader_yrec provides a means of reading in .track, .last, and .store files as pandas dataframes or astropy tables. Provides a python interface for loading YREC data products.

## newheader_yrec:
Provides the user with a modified wrthead.f file, to be used in the compiling/recompiling process. Allows for the generation of output files in a format that is better suited to reading into pandas, astropy.table, etc. and other modern astronomical data analysis tools for python. 

## change_nml: 
YREC utilizes two namelists, one is a nml1 which controls settings, primes models, and provides paths to the correct places where the code is to output the results of a run as well as where the input files of equations of state, physics, opacities, etc are stored. change_nml allows the user to change all the filepaths in a directory of namelists to the approriate matching files in the directory where YREC is stored. The YREC directory tree for input files specifically must remain as downloaded for it to work. 

