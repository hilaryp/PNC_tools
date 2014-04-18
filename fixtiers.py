#!/usr/bin/env python
# Copyright (c) 2014 Hilary Prichard
#
# Uses textgrid.py methods to fix tier ordering problems in the PNC 
# Download textgrid.py from https://github.com/kylebgorman/textgrid
# USAGE1: python fixtiers.py -g inputlist.txt > tiers.txt
# USAGE2: python fixtiers.py -f inputlist.txt newtiers.txt outputlist.txt

from sys import argv
from textgrid import TextGrid, TextGridFromFile
from getopt import getopt, GetoptError

def getWrongTiers(source):
    """Takes list of TextGrids, returns text file list of tiers in each"""
    for line in source.readlines():
        f = line.rstrip('\n')
        tg = TextGridFromFile(f)
        tiers = tg.getNames()
        print tiers

def fixTiers(source, tierlist, outfile):
    """Takes list of TextGrids, file with new tier orders, list of output file
    names, returns TextGrids with new tier order"""
    for line, tier, out in zip(source.readlines(), tierlist, outfile.readlines()):
            f = line.rstrip('\n')
            oldtg = TextGridFromFile(f)
            list_from_file = eval(tier)
            output = out.rstrip('\n')
            newtg = TextGrid('newtg')
            for n in list_from_file:
                ntier = oldtg.getFirst(n)
                newtg.append(ntier) 
            newtg.write(output)

if __name__ == '__main__':
    infile = None
    newtiers = None
    try:
        (opts, args) = getopt(argv[1:], 'g:f:', ['get-tiers=', 'fix-tiers='])
        for (opt, val) in opts:
            if opt in ('-g', '--get-tiers') :
                infile = val
                with open(infile, 'rU') as source:
                    getWrongTiers(source)
            elif opt in ('-f', '--fix-tiers'):
                infile = val
                newtiers, outfiles = args
                with open(newtiers, 'rU') as tierlist, open(outfiles, 'r') as outfile, open(infile, 'r') as source:
                    fixTiers(source, tierlist, outfile)
            else:
                raise GetoptError
    except GetoptError, err:
        exit(err)
    
