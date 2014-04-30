PNC\_tools
=========

This repository contains various scripts for working with Philadelphia 
Neighborhood Corpus (PNC) data. Please consult the 
[wiki](https://github.com/hilaryp/PNC_tools/wiki) 
for detailed usage information for each script.

## extractFormants-noprompt.py

An alternative to the version of `extractFormants.py` currently
distributed with the [FAVE](https://github.com/JoFrhwld/FAVE) suite. It allows
users to automatically supply the demographic information used in formant 
extraction via a .csv file, rather than through the usual terminal prompts.  

## plt2csv.py

Takes a Plotnik file (.plt or .pll) created by FAVE-extract and 
converts it to a .csv file. All plotnik codes are translated into more 
user-friendly labels. Original code by 
[Kyle Gorman](https://github.com/kylebgorman). 

## fixtiers.py

Uses [textgrid.py](https://github.com/kylebgorman/textgrid) methods
to manually fix tier ordering in PNC textgrids. Useful for running FAVE-extract
in batch mode, which by default extracts the first tier.
