#!/usr/bin/env python2.7

# C.D. Warman
# October 16, 2017

# This script converts .gaf files (gene annotation file) into formatted input
# for the R package topGO. The .gaf file must be in descending order by gene
# id (column 2) then go_term (column 5).

# Usage:
# gaf_converter.py [imput_file.gaf]

import sys
import io

# Making some lists for the input file
gene_id_list = list()
go_term_list = list()

# Opening the input file
fandle = io.open(sys.argv[1], "rU")
for line in fandle:
    linestripped = line.strip()
    line_list = linestripped.split("\t")
    if (len(line_list) > 5) and (line_list[0] != "!db"):
        gene_id = line_list[1]
        go_term = line_list[4]
        gene_id_list.append(gene_id)
        go_term_list.append(go_term) 
fandle.close()

# Setting up some lists for the loop
previous_gene_id = "start"
final_gene_id_list = list()
final_go_term_list = list()
temp_go_term_list = list()

# This loop goes through each line of both gene and go term lists. For each
# gene, it adds all the go terms for that gene to a list. Finally, it adds this
# list to a list of lists of go terms, one list of go terms for each gene.
for line in range(len(gene_id_list)):
    current_gene_id = gene_id_list[line]
    current_go_term = go_term_list[line]
    if line == 0: 
        temp_go_term_list.append(current_go_term)
        previous_gene_id = current_gene_id
    elif line == (len(gene_id_list) - 1):
        if current_gene_id != previous_gene_id:
            final_gene_id_list.append(previous_gene_id)
            final_go_term_list.append(temp_go_term_list)
            temp_go_term_list = list()
            temp_go_term_list.append(current_go_term)
            final_gene_id_list.append(current_gene_id)
            final_go_term_list.append(temp_go_term_list)
        else:
            final_gene_id_list.append(current_gene_id)
            temp_go_term_list.append(current_go_term)
            final_go_term_list.append(temp_go_term_list)
    else:
        if current_gene_id != previous_gene_id:
            final_go_term_list.append(temp_go_term_list)
            temp_go_term_list = list()
            final_gene_id_list.append(previous_gene_id)
            previous_gene_id = current_gene_id
        temp_go_term_list.append(current_go_term)

# Printing the output
out_fandle = io.open("output.txt", "wb")
for x in range(len(final_go_term_list)):
    if len(final_go_term_list[x]) == 1:
        out_fandle.write(str(final_gene_id_list[x]) +
                             "\t" +
                             str(final_go_term_list[x])[3:-2] +
                             "\n")
    else:
        # Turning the list of GO terms into a string separated by commas and a space
        output_go_term_line = ", ".join(final_go_term_list[x])
        out_fandle.write(str(final_gene_id_list[x]) + 
                             "\t" + 
                             output_go_term_line +
                             "\n")
out_fandle.close()













