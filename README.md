# YREC-Wrappers
Wrappers, helpful codes, and additional machinery to interface with YREC with languages such as Python

Tracker.py is a program written to read in .track files for YREC. Its structure can be easily adapted for .store files and .last files as well. 

To modify for other purposes, open the .store or .last file and find a consistent keyword in the header to denote where the file/table begins. For .track files its the string '#Version' for exmaple. 

This lets the code to calculate where to begin reading and accurately parse the tables. 

Needs the updated wrthead.f file in YREC. To use tracker to read in files as pandas or astropy tables, replace the old YREC wrthead.f file with this one and then recompile the program.
