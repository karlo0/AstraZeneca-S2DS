#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 08:36:57 2019
@author: team astrazeneca
"""

"""
script to extract disease names from human_disease_ontology.txt into a csv file.

human_disease_ontology.txt was obtained from http://disease-ontology.org/downloads/ (sourceforge)
"""
# extract disease names into a list
disease_names = [];
with open ('human_disease_ontology.txt', 'rt') as input_file: # Open file human_disease_ontology.txt
    for line in input_file: # Store each line in str line
        if 'name:' in line:
            new_disease_name = line[6:len(line)-1] #last character is /n
            disease_names.append(new_disease_name)

print(disease_names) # just to check

# convert the list into a csv file
import csv
with open('diseases.csv', "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for value in disease_names:
        writer.writerow([value])