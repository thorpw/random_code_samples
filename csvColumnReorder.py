#!/usr/bin/env

#Script to read in a file, reorder columns based on specified order and write to new file. If the file is not empty.

####################################
# File name: csvColumnReorder.py   #
# Date created: 15/5/2018          #
# Author: Warren Thorp             #
# Date last modified: 15/5/2018    #
# Python Version: 3.6              #
####################################

import csv
import os

# check if there is any data in the received file from Gobalto
if os.stat(r'C:\Users\ThorpWa\Documents\column_reorder_test\gobaltoFileEmpty.csv').st_size == 0:
    with open(r'C:\Users\ThorpWa\Documents\column_reorder_test\studies.csv', 'r', encoding='utf8') as infile, \
    open(r'C:\Users\ThorpWa\Documents\column_reorder_test\gobaltoFileReordered.csv', 'w+') as outfile:
        # output dict needs a list for new column ordering
        fieldnames = ['column', 'This', 'is', 'reordered', 'now']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, extrasaction='raise', lineterminator='\n')
        # reorder the header first 
        writer.writeheader()
        for row in csv.DictReader(infile):
            # writes the reordered rows to the new file
            writer.writerow(row)
