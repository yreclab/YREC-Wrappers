
YREC Header Changes

By Vince Smedile - Ohio State

Tracker.py is a program written to read in .track files for YREC. Its structure can be easily adapted for .store files and .last files as well. 

To modify for other purposes, open the .store or .last file and find a consistent keyword in the header to denote where the file/table begins. For .track files its the string '#Version' for exmaple. 

This lets the code to calculate where to begin reading and accurately parse the tables. 