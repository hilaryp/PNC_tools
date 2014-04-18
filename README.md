PNC\_tools
=========

This repository contains various scripts for working with Philadelphia 
Neighborhood Corpus (PNC) data. 

## plt2csv.py

This script takes a Plotnik file (.plt or .pll) created by FAVE-extract and 
converts it to a .csv file. All plotnik codes are translated into more 
user-friendly labels. Original code by 
[Kyle Gorman](https://github.com/kylebgorman). 

### Usage
Single file:

    python plt2csv.py input.plt > output.csv

Or to concatenate all your .plt files into one .csv:

    python plt2csv.py input/*.plt > output.csv

Use `-d` to include columns for the demographic information given in the .plt 
header line. Only recommended if using your own files; existing PNC file 
headers are often inconsistent.

    python plt2csv.py -d input/*.plt > output.csv

### Output
If the input filename follows the PNC format, it is parsed to return Subject 
ID as the first column. Otherwise Subject ID defaults to the filename, 
stripped of path and extension. An example:
    
    File: PH13-1-1-HilaryP-rx.plt

    Subject,Speaker,F1,F2,F3,Word,Stress,Duration,VClass,Manner,Place,Voice,PreSeg,FolSeq,F1_20,F2_20,F1_35,F2_35,F1_50,F2_50,F1_65,F2_65,F1_80,F2_80
    PH13-1-1,Hilary P,772.8,1277.2,3561.1,ONE,1,130,uh,nasal,alveolar,voiced,glide,<n.a.>,795.0,1191.0,772.0,1284.0,768.0,1378.0,767.0,1462.0,740.0,1599.0
    PH13-1-1,Hilary P,468.7,2008.6,2505.0,TWO,1,200,Tuw,<n.a.>,<n.a.>,<n.a.>,oral alveolar,<n.a.>,439.0,1972.0,430.0,1892.0,420.0,1820.0,419.0,1697.0,422.0,1583.0

## fixtiers.py

This script uses [textgrid.py](https://github.com/kylebgorman/textgrid) methods
to manually fix tier ordering in PNC textgrids. Useful for running FAVE-extract
in batch mode, which by default extracts the first tier.

### Usage
There are two modes specified by option flags.

(1) Get tiers:

    python fixtiers.py -g inputlist.txt > tiers.txt

(2) Fix tiers:
    
    python fixtiers.py -f inputlist.txt newtiers.txt outputlist.txt

The get-tiers mode takes as its input a list of textgrid files and outputs a 
list of each file's tiers. The user can then manually reorder these tiers in 
the text file and save the new order for input to the fix-tiers mode. 

The fix-tiers mode takes as its input (1) the list of textgrid files, (2) the 
list of new tier orders, (3) a list of output filenames, and outputs new 
textgrids with the specified tier order and filename. 

Input list example:
    
    /User/textgrids/PH14-1-1-Bob.TextGrid
    /User/textgrids/PH14-1-2-Joy.TextGrid

Tier list example:

    [u'Bob - phone', u'Bob - word', u'Noise - phone', u'Noise - word']
    [u'Joy - phone', u'Joy - word', u'Noise - phone', u'Noise - word'] 
