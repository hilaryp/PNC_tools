PNC\_tools
=========

This repository contains various scripts for working with Philadelphia Neighborhood Corpus (PNC) data. 

## plt2csv.py

This script takes a plotnik file (.plt or .pll) created by FAVE-extract and converts it to a .csv file. All plotnik codes
are translated into more user-friendly labels. 

### Usage
Single file:

    python plt2csv.py input.plt > output.csv

Or to concatenate all your .plt files into one .csv:

    python plt2csv.py input/*.plt > output.csv

### Output
`plt2csv.py` is currently written for use with PNC-style filenames, but can easily be modified as needed. The input filename is parsed to return Subject ID as the first column. An example:
    
    File: PH13-1-1-HilaryP-rx.plt

    Subject,Speaker,F1,F2,F3,Word,Stress,Duration,VClass,Manner,Place,Voice,PreSeg,FolSeq,F1_20,F2_20,F1_35,F2_35,F1_50,F2_50,F1_65,F2_65,F1_80,F2_80
    PH13-1-1,Hilary P,772.8,1277.2,3561.1,ONE,1,130,uh,nasal,alveolar,voiced,glide,<n.a.>,795.0,1191.0,772.0,1284.0,768.0,1378.0,767.0,1462.0,740.0,1599.0
    PH13-1-1,Hilary P,468.7,2008.6,2505.0,TWO,1,200,Tuw,<n.a.>,<n.a.>,<n.a.>,oral alveolar,<n.a.>,439.0,1972.0,430.0,1892.0,420.0,1820.0,419.0,1697.0,422.0,1583.0

The output .csv does not currently include the demographic information given in the .plt header line. In the event you wish to use that information, comment out lines 87 and 128-134, then uncomment lines 90-92 and 137-143. 
