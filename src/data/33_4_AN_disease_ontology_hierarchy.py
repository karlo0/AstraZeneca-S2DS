#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Begun on Wed Mar 18 14:30:13 2019

@author: nLp ATTACK

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS

mesh_df = pd.read_pickle('../../data/final/mesh.pkl') # read the mesh database pkl file

def convert_meshid_to_tree_numbers(mesh_id):
    """
    converts any mesh_id to all its tree numbers using the mesh database (mesh.pkl)
    str -> list
    Examples:        
        >>> convert_meshid_to_tree_numbers('D000013')
        >>> ['C16.131']
        
        >>> convert_meshid_to_tree_numbers('D000001')
        >>> ['D03.633.100.221.173']
        
        >>> convert_meshid_to_tree_numbers('D000002')
        >>> ['D02.705.400.625.800', 'D02.705.539.345.800', 'D02.886.300.692.800']
              
        >>> convert_meshid_to_tree_numbers('D000012')
        >>> ['C16.320.565.398.500.440.500', 'C18.452.584.500.875.440.500', 'C18.452.648.398.500.440.500']
        
        >>> convert_meshid_to_tree_numbers('D000016')
        >>> ['C16.131.080', 'C26.733.031', 'G01.750.748.500.031', 'N06.850.460.350.850.500.031', 'N06.850.810.300.360.031']

        >>> convert_meshid_to_tree_numbers('D0000020')
        >>> []
        
        >>> convert_meshid_to_tree_numbers('A0000020')
        >>> []
    """
    # get the row indexes for the mesh id
    row_indexes = mesh_df.index[mesh_df['mesh_id'] == mesh_id].tolist()    
    tree_numbers = [] # initialize a list to append the tree numbers
    for row_index in row_indexes:
        tree_num = mesh_df.loc[row_index,'mesh_treenumbers']
        tree_numbers.append(tree_num)
    return tree_numbers

def convert_treenumber_to_parent_tree_hierarchy(tree_number):
    """
    takes a treenumber and converts it into its parent tree hierarchy of mesh_headings.
    the topmost mesh heading in the hierarchachy is the first entry followed by the 
    next one and so on till the mesh heading for the input tree number
    str -> list
    Examples:
        >>> convert_treenumber_to_tree_hierarchy('N06.850.460.350.850.500.031')
        >>> ['Environment and Public Health', 'Public Health', 'Environmental Pollution',
             'Environmental Exposure', 'Radiation Exposure', 'Radiation Injuries',
             'Abnormalities, Radiation-Induced']
        {Note: 'N06.850.460.350.850.500.031' = Abnormalities, Radiation-Induced}
        
        >>> convert_treenumber_to_tree_hierarchy('C26.733.031')
        >>> ['Wounds and Injuries', 'Radiation Injuries', 'Abnormalities, Radiation-Induced']
        
        >>> convert_treenumber_to_tree_hierarchy('C16.131')
        >>> ['Congenital, Hereditary, and Neonatal Diseases and Abnormalities', 'Congenital Abnormalities']
    
        >>> convert_treenumber_to_tree_hierarchy('C18.452.584.500.875.440.500')
        >>> ['Nutritional and Metabolic Diseases', 'Metabolic Diseases', 'Lipid Metabolism Disorders',
             'Dyslipidemias', 'Hypolipoproteinemias', 'Hypobetalipoproteinemias', 'Abetalipoproteinemia']

        >>> convert_treenumber_to_tree_hierarchy('D09.067.342.356.050')
        >>> ['Carbohydrates', 'Amino Sugars', 'Hexosamines', 'Galactosamine', 'Acetylgalactosamine']
    
    """
    # make list of parents' tree numbers
    all_parents = [];
    for i in range(0,len(tree_number), 4):
        all_parents.append((tree_number[0:i+3]))
    hierarchy_list = [];
    for parent in all_parents:                               
        row_index = mesh_df.index[mesh_df['mesh_treenumbers'] == parent].values[0]
        hierarchy_list.append(mesh_df.loc[row_index,'mesh_heading'])
    return(hierarchy_list)

## initialize dictionary for storing disease counts
#id_name_tree_df_temp = id_name_tree_df[id_name_tree_df.category=='C'] # only disease category
#new_dict = {}
#for item in id_name_tree_df_temp.mesh_heading:
#    new_dict[item] = 0

## count the entries
#pmid_df = pd.read_pickle('../../data/final/geo.pkl')
##for row_index in range(0,len(pmid_df['mesh_id'])):
##for row_index in range(0,10000):
#for row_index in range(0,200):
#    all_ids_row_index = pmid_df.loc[row_index,'mesh_id']        
#    all_hierarchies = []
#    for id_row_index in all_ids_row_index:        
#        tree_numbers_id = convert_meshid_to_tree_numbers(id_row_index)
##        print(tree_numbers_id)
#        for tree_number in tree_numbers_id:            
#            if tree_number[0] == 'C':
#                hierarchy = convert_treenumber_to_tree_hierarchy(tree_number)
##                print(hierarchy)
#                if not hierarchy[0].startswith('Pathological'):                    
#                    for item in hierarchy:
#                        all_hierarchies.append(item)
#                        s = set(all_hierarchies)
#                        print(s)
#                        for item in s:
#                            new_dict[item] = new_dict[item] + 1
#        
#        
# 
##max(A, key=A.get)
#from collections import Counter
#print(Counter(new_dict).most_common(15))
       
"""
# * = * = * = * = * = # code for Luis' graph  = * = * = * = * = * = * = * = * = #

# objective is to produce csv file with column1 = disease_tree_id and column2 = parent_tree_id
# for entire database
#pmid_df = pd.read_pickle('../../data/final/geo.pkl')
#disease_pmid_df = pmid_df[pmid_df.category=='C'] # select only diseases
## set up disease vocabulary subset df of main mesh df
disease_id_name_tree_df = id_name_tree_df[id_name_tree_df.category=='C'] # only disease category

# initialize
all_records = []
#disease_id_name_tree_df = disease_id_name_tree_df.iloc[0:3,] # only for testing
# go through the entire input data
for row_index, row in disease_id_name_tree_df.iterrows():
    # find all tree numbers corresonding to the mesh_id for that row
    # (each mesh_id may often have multiple tree numbers)
    all_tree_numbers = convert_meshid_to_tree_numbers(disease_id_name_tree_df.loc[row_index,'mesh_id'])        
    # iterate over the tree_numbers
    for tree_number in all_tree_numbers:
        if tree_number[0] == 'C': # additional check to ensure only diseases are selected
            parent_tree_number = tree_number[0:-4] # select parent tree number       
            all_records.append([tree_number, parent_tree_number]) # append to record

import csv
import os

def WriteListToCSV(csv_file,csv_columns,data_list):    
    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(csv_columns)
        for data in data_list:
            writer.writerow(data)    
    return            

csv_columns = ['Diease_TreeNumber','Parent_TreeNumber']
csv_data_list = all_records

currentPath = os.getcwd()
csv_file = "disease_parent.csv"

WriteListToCSV(csv_file,csv_columns,csv_data_list)

"""

"""

# * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = #
# * = * = * = * = * = * = * = * Archives * = * = * = * = * = * = * = * = * = #
# * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = #
    
   
# this function is deprecated because it uses SlimMappings given in MEDIC vocabulary.
# unfortunately the Slimmappings were not accurate and omitted important information.
# e.g., the disease tag Diabetic Nephropathies with the disease ID D003928 had the hierarchy 
# (read top-down) ['Urogenital disease (male)', 'Urogenital disease (female)', 'Endocrine system disease', 'Diabetic Nephropathies']
# but this does not include diabetes or diabetes mellitus!
#def match_mesh_disease_id_to_disease_hierarchy(diseases_vocab_df, mesh_id):
#    for index, row in diseases_vocab_df["DiseaseID"].iteritems():
#        if mesh_id in row:
#            disease_name = diseases_vocab_df.loc[index, "DiseaseName"]
#            disease_hierarchy_temp = diseases_vocab_df.loc[index, "SlimMappings"]
#            disease_hierarchy = [];
#            index1 = 0
#            for index2, character in enumerate(disease_hierarchy_temp):
#                if character == '|':
#                    disease_hierarchy.append(disease_hierarchy_temp[index1:index2])
#                    index1 = index2+1
#            disease_hierarchy.append(disease_hierarchy_temp[index1:])
#            disease_hierarchy.reverse()
#            disease_hierarchy.append(disease_name)
#            
#            return True, index, disease_name, disease_hierarchy
#    return False
#
#import pandas as pd
#ctd_diseases_df = pd.read_csv('../data/external/CTD_diseases.csv')
#
#(value, index, disease_name, disease_hierarchy) = match_mesh_disease_id_to_disease_hierarchy(ctd_diseases_df, 'D003928')
#
#print(disease_hierarchy)

"""