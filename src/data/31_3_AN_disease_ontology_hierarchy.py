#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Begun on Wed Mar 18 14:30:13 2019

@author: nLp ATTACK

"""
import pandas as pd
id_name_tree_df = pd.read_pickle('../../data/processed/id_name_tree_without_SCR.pkl')

def convert_diseaseid_to_tree_numbers(diseaseid):
    row_indexes = id_name_tree_df.index[id_name_tree_df['mesh_id'] == diseaseid].tolist()
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
    
##data_df = pd.read_pickle('disease_tags_dnorm_advanced.pkl')
#df = pd.read_pickle('disease_tags.pkl')

disease_id = 'D000121'
all_tree_numbers = convert_diseaseid_to_tree_numbers(disease_id)
print(all_tree_numbers)
for tree_number in all_tree_numbers:
    print(convert_treenumber_to_tree_hierarchy(tree_number))
    
    
#id_name_tree_df = pd.DataFrame([{'id': 'D000001',  'Name': 'Calcimycin', 'TreeNumbers': 'D03.633.100.221.173'},
#         {'id': 'D000002',  'Name': 'Temefos',  'TreeNumbers': 'D02.705.400.625.800'},
#         {'id': 'D000002',  'Name': 'Temefos',  'TreeNumbers': 'D02.705.539.345.800'},
#         {'id': 'D000002',  'Name': 'Temefos',  'TreeNumbers': 'D02.886.300.692.800'},
#         {'id': 'D000003',  'Name': 'Abattoirs',  'TreeNumbers': 'J01.576.423.200.700.100'},
#         {'id': 'D000003',  'Name': 'Abattoirs',  'TreeNumbers': 'J03.540.020'},
#         {'id': 'D000004',  'Name': 'Abbreviations as Topic',  'TreeNumbers': 'L01.559.598.400.556.131'}])

    
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







