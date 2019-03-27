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

# read the mesh database pkl file
id_name_tree_df = pd.read_pickle('../../data/final/id_name_tree_without_SCR.pkl')

# takes a meshid and converts it into tree numbers
def convert_meshid_to_tree_numbers(mesh_id):
    row_indexes = id_name_tree_df.index[id_name_tree_df['mesh_id'] == mesh_id].tolist()
    # append the tree numbers to a list
    tree_numbers = []
    for row_index in row_indexes:
        tree_num = id_name_tree_df.loc[row_index,'mesh_treenumbers']
        tree_numbers.append(tree_num)
    return tree_numbers

def convert_treenumber_to_tree_hierarchy(tree_number):
    all_parents = [];
    for i in range(0,len(tree_number), 4):
        all_parents.append((tree_number[0:i+3]))        
    hierarchy_list = [];
    for parent in all_parents:                               
        row_index = id_name_tree_df.index[id_name_tree_df['mesh_treenumbers'] == parent].values[0]
        hierarchy_list.append(id_name_tree_df.loc[row_index,'mesh_heading'])
    return(hierarchy_list)
 
pmid_df = pd.read_pickle('../../data/final/geo_id_mesh_from_pmid.pkl')

id_name_tree_df_temp = id_name_tree_df[id_name_tree_df.category=='C'] # only disease category

new_dict = {}
for item in id_name_tree_df_temp.mesh_heading:
    new_dict[item] = 0

count = 0
for row_index in range(0,len(pmid_df['mesh_uis'])):
#for row_index in range(0,100):
#for row_index in range(0,1):
    all_ids_row_index = pmid_df.loc[row_index,'mesh_uis']        
    all_hierarchies = []
    for id_row_index in all_ids_row_index:        
        tree_numbers_id = convert_meshid_to_tree_numbers(id_row_index)        
        for tree_number in tree_numbers_id:            
            if tree_number[0] == 'C':
                hierarchy = convert_treenumber_to_tree_hierarchy(tree_number)                               

                if not hierarchy[0].startswith('Pathological'):
                    count+=1
                    for item in hierarchy:
                        all_hierarchies.append(item)
                        s = set(all_hierarchies)
    for item in s:
        new_dict[item] = new_dict[item] + 1

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







