#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Begun on Wed Mar 18 14:30:13 2019

@author: nLp ATTACK

"""
import pandas as pd
id_name_tree_df = pd.read_pickle('../data/processed/id_name_tree.pkl')

all_tree_numbers = id_name_tree_df['TreeNumbers']
def convert_treenumber_to_tree_hierarchy(tree_number):
    hierarchy_list = [];
    for i in range(0,len(tree_number), 4):
        print(tree_number[0:i+3])
        tree_number_portion = (tree_number[0:i+3]) + '\n'
        for index, item in enumerate(all_tree_numbers):
            if tree_number_portion in item:                
                hierarchy_list.append(id_name_tree_df.loc[index,'Name'])
    return(hierarchy_list)
    
print(convert_treenumber_to_tree_hierarchy('D08.811.277.450.430.700.750.111\n'))

#import pickle
#data_df = pd.read_pickle('disease_tags_dnorm_advanced.pkl')
df = pd.read_pickle('disease_tags.pkl')

D009091

    
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







