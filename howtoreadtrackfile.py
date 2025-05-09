# Listed here is a short script for using the new wrthead.f header for .track files in YREC.
# The new header is toggleable and can be commented out as needed
# Makes it possible to use python Pandas DataFrames using pandas.read_csv() out of .track files

# After building YREC with the new wrthead.f file you can run something like the following to read in the .track files: 

# This part identifies the start of the table/headers and informs pandas how many lines to skip
 start = []
    with open(file, 'r') as fp:
        lines = fp.readlines()
        fp.close()
        for row in lines:
            word = '#Version'
            if row.find(word) != -1:
                # Start is a the row you start on
                start.append(lines.index(row))
# Then you can easily read in the files
track = pd.read_csv(file, header ='infer',
                    skiprows = start[-1]+1, sep='\s+', float_precision= 'legacy')