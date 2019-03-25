#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Begun on Wed Mar 18 14:30:13 2019

@author: nLp ATTACK

"""
import pandas as pd
id_name_tree_df = pd.read_pickle('../../data/processed/id_name_tree.pkl')


id_name_tree_df = pd.DataFrame([{'id': 'D000001',  'Name': 'Calcimycin', 'TreeNumbers': 'D03.633.100.221.173'},
         {'id': 'D000002',  'Name': 'Temefos',  'TreeNumbers': 'D02.705.400.625.800'},
         {'id': 'D000002',  'Name': 'Temefos',  'TreeNumbers': 'D02.705.539.345.800'},
         {'id': 'D000002',  'Name': 'Temefos',  'TreeNumbers': 'D02.886.300.692.800'},
         {'id': 'D000003',  'Name': 'Abattoirs',  'TreeNumbers': 'J01.576.423.200.700.100'},
         {'id': 'D000003',  'Name': 'Abattoirs',  'TreeNumbers': 'J03.540.020'},
         {'id': 'D000004',  'Name': 'Abbreviations as Topic',  'TreeNumbers': 'L01.559.598.400.556.131'}])

def convert_diseaseid_to_tree_numbers(diseaseid):
    row_index_list = id_name_tree_df.index[id_name_tree_df['id'] == diseaseid].tolist()    
    disease_hierarchy_list = []
    for row_index in row_index_list:
        tree_number = id_name_tree_df.loc[row_index,'TreeNumbers']
        disease_hierarchy_list.append(tree_number)
    return disease_hierarchy_list

def convert_treenumber_to_parents(tree_number):
    parents_list = [];
    for i in range(0,len(tree_number), 4):
        parents_list.append((tree_number[0:i+3]))
    return parents_list    

##data_df = pd.read_pickle('disease_tags_dnorm_advanced.pkl')
#df = pd.read_pickle('disease_tags.pkl')

#all_tree_numbers = id_name_tree_df['TreeNumbers']
#    hierarchy_list = [];
#
#        for index, item in enumerate(all_tree_numbers):
#            if tree_number_portion in item:                
#                hierarchy_list.append(id_name_tree_df.loc[index,'Name'])
#    return(hierarchy_list)

#print(convert_treenumber_to_tree_hierarchy('D08.811.277.450.430.700.750.111\n'))
#

disease_id = 'D000003'

tree_numbers_list = convert_diseaseid_to_tree_numbers('D000003')
print(tree_numbers_list)
for tree_number in tree_numbers_list:
    print(convert_treenumber_to_parents(tree_number))

    
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







