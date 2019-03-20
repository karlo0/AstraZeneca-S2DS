#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Begun on Mon Mar 18 14:30:13 2019

@author: nLp ATTACK

"""
import pandas as pd

# initialize
id_name_tree_df = pd.DataFrame([], columns=['Id','Name', 'ParentTreeNumbers'])
id_name_tree_dict = {}
tree_value = []

with open('../data/external/d2019_expt.txt') as f:    
    for line in f: # cycle through each line
        if line.startswith('MH = '): # name
            id_name_tree_dict['Name'] = line[5:-1]
        
        if line.startswith('MN = '): # tree numbers
            # collect tree number for each line            
            tree_value_temp = line[5:] 
            # include last char \n because it will help to search each level of the tree
            # collect all tree numbers
            tree_value.append(tree_value_temp)
            
        id_name_tree_dict['ParentTreeNumbers1'] = tree_value       
               
        if line.startswith('UI = '): # unique id
            tree_value = [] # initialize since all tree numbers are obtained
            id_name_tree_dict['Id'] = line[5:-1]
            id_name_tree_df = id_name_tree_df.append(id_name_tree_dict, ignore_index=True)            

print(id_name_tree_df)





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







