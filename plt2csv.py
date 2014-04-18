#!/usr/bin/env python
# Copyright (c) 2013 Kyle Gorman
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# plt2csv.py: convert Plotnik token files to CSV token files
# Kyle Gorman <gormanky@ohsu.edu>
#
# additional edits by Hilary Prichard <hilaryp@ling.upenn.edu>
#
# By default (and sanely enough), Python assumes that files use the
# platform-specific newline delimiters: for most users, this will be
# '\n'. However, many Plotnik files were made on different platforms (
# particularly early, pre-OS X Macintoshes, which used '\r' as the newline
# delimiter). Therefore, this program uses Python's "universal newline"
# mode, which should work with any likely configuration.
#
# See "USAGE" below for more information
#
# 2013-12-2 update: added handling for FAVE's new multiple measurement
# output. New columns for F1 and F2 at 20, 35, 50, 65, and 80%. Also
# updated subject name regex to accommodate non PH-series data. Updates
# after this are reflected in git commit history. -HEP

from __future__ import with_statement  # Python 2.5 compatibility

from os import path
from re import match
from csv import DictWriter
from sys import argv, stdout
from itertools import islice
from getopt import getopt, GetoptError

NAN = float('nan')
USAGE = 'USAGE: {} < PLT > CSV'.format(__file__)
DELIMITER = ','
SUBJECT = r'^\D\D\D?\d?\d?-\D?\d?\d?-\d\d?'
# works for PH- IHP- and PHI-series files

VCLASSES = {1: 'i', 2: 'e', 3: 'ae', 5: 'o', 6: 'uh', 7: 'u', 11: 'iy',
            12: 'iyF', 14: 'iyr', 21: 'ey', 22: 'eyF', 24: 'eyr',
            33: 'aeh', 39: 'aeBR', 41: 'ay', 42: 'aw', 43: 'ah', 44: 'ahr',
            47: 'ay0', 53: 'oh', 54: 'ohr', 61: 'oy', 62: 'ow', 63: 'owF',
            64: 'owr', 72: 'uw', 73: 'Tuw', 74: 'uwr', 82: 'iw', 94: '*hr'}
MANNERS = {0: '<n.a.>', 1: 'stop', 2: 'affricate', 3: 'fricative',
           4: 'nasal', 5: 'lateral', 6: 'rhotic'}
# changed: "central" (huh?) to "rhotic" --KBG
PLACES = {0: '<n.a.>', 1: 'labial', 2: 'labiodental', 3: 'interdental',
          4: 'alveolar', 5: 'alveopalatal', 6: 'velar'}
# changed: "apical" to "aveolar" (this isn't Belfast) and "palatal" to
# "alveopalatal" (this isn't Beijing) --KBG
VOICES = {0: '<n.a.>', 1: 'voiceless', 2: 'voiced'}
PRE_SEGS = {0: '<n.a.>', 1: 'oral labial', 2: 'm', 3: 'oral alveolar',
            4: 'n', 5: 'alveopalatal', 6: 'velar', 7: 'liquid',
            8: 'obstruent-liquid', 9: 'glide'}
# changed: "nasal labial" to "m" (it's the only one), "apical" to "oral
# alveolar" (as [n] is not included), "nasal apical" to "n" (it's the only
# one), "palatal" to "alveopalatal" (that's what it is), "obstruent liquid"
# to "obstruent-liquid" (to make it clear that's a sequence we're talking
# about), and "w/y" to "glide" --KBG
FOL_SEQS = {0: '<n.a.>', 1: '1.fol.syl', 2: '2.fol.syl', 3: 'complex',
            4: '1.fol.syl.complex', 5: '2.fol.syl.complex'}
# changed: simplified the format overall here, should be transparent


def plt2csv(source, sink, subject):
    """
    Parse an individual Plotnik file handle (stream) and print tokens to an
    csv.DictWriter (sink) according to a specification provided by HEP.
    I don't bother with float or integer conversion except when it matters
    """
    # first line of header
    (s, a, x, e, c, n, y) = source.readline().rstrip().split(DELIMITER)
    
    row = {'Subject': subject, 'Speaker': s.strip()}

    if demographics:
        row = {'Subject': subject, 'Speaker': s.strip(), 'Age': a, 'Sex': x, 
               'Ethnicity': e, 'Schooling': c if c != '' else NAN, 
               'Neighborhood': n, 'Year': y}

    # tells us where "summary" begins
    n_rows = int(source.readline().split(',')[0])
    for (i, line) in enumerate(islice(source, 0, n_rows)):
        (F1, F2, F3, ve, sd, wp) = line.rstrip().split(DELIMITER, 5)[:6]
        row['F1'] = F1
        row['F2'] = F2
        row['F3'] = F3
        # backwards compatibility for old FAVE-extract files
        if wp[-1] == '>':
            # separate word + plotnik junk out from vowel trajectories
            # this is ugly, but number of fields in `wp` is not constant:
            # "WORD {opt glide code} /nFormants/ timestamp <trajectory>"
            (w, vt) = wp.split('<', 1)
            row['Word'] = w.split(None)[0]
            (row['F1_20'], row['F2_20'], row['F1_35'], row['F2_35'],
             row['F1_50'], row['F2_50'], row['F1_65'], row['F2_65'],
             row['F1_80'], row['F2_80']) = vt.rstrip('>').split(',')
        else:
            # no extra measurements in old files
            row['Word'] = wp.split(None)[0]
        # bizarrely, stress and duration are coded in the same column
        (s, d) = sd.split('.', 2)
        row['Stress'] = s
        row['Duration'] = d
        # same for vowel class and environmental coding
        (vc, ec) = ve.split('.', 2)
        row['VClass'] = VCLASSES[int(vc)]
        (m, pl, v, ps, f) = (int(i) for i in ec)  # decompose that sucker
        row['Manner'] = MANNERS[m]
        row['Place'] = PLACES[pl] if pl in PLACES else NAN
        row['Voice'] = VOICES[v]
        row['PreSeg'] = PRE_SEGS[ps]
        row['FolSeq'] = FOL_SEQS[f]
        # write out
        sink.writerow(row)


if __name__ == '__main__':
    # command line option to include demographic info given in plt header
    demographics = False
    try:
        (opts, args) = getopt(argv[1:], 'd')
        for (opt, val) in opts:
            if opt == '-d':
                demographics = True
            else:
                raise GetoptError
    except GetoptError, err:
        exit(err)

    # turn STDOUT into a DictWriter
    fields_IDs = ['Subject', 'Speaker']
    fields_demographics = ['Age', 'Sex', 'Ethnicity', 'Schooling',
                           'Neighborhood', 'Year'] if demographics else []
    fields_measures = ['F1', 'F2', 'F3', 'Word',
                       'Stress', 'Duration', 'VClass',
                       'Manner', 'Place', 'Voice',
                       'PreSeg', 'FolSeq', 'F1_20', 'F2_20',
                       'F1_35', 'F2_35', 'F1_50', 'F2_50',
                       'F1_65', 'F2_65', 'F1_80', 'F2_80']
    sink = DictWriter(stdout, fieldnames=fields_IDs + fields_demographics + 
                      fields_measures)
    sink.writeheader()
    # run it
    for fname in args:
        try:
            subject = match(SUBJECT, path.split(fname)[1]).group(0)
        # If filename isn't PNC-style, default to subject = filename
        except AttributeError:
            subject = path.splitext(path.split(fname)[1])[0]
        finally:
            with open(fname, 'rU') as source:
                plt2csv(source, sink, subject)
