#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Begun on Wed Mar 18 14:30:13 2019

@author: nLp ATTACK

"""
import pandas as pd

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







