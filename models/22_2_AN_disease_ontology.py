#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Begun on Mon Mar 18 14:30:13 2019

@author: nLp ATTACK

"""
import pandas as pd
import pickle
id_name_tree_df = pd.read_pickle('../data/processed/id_name_tree.pkl')

#k = (df.Id[df.Id == id_tag].index.tolist())

tree_tag1 = 'D08.811.277.450.430.700.750.111'

#tree_tag_list = []
#tree_tag_list.append(tree_tag)
#hierarchy_tags = [];
#for i in range(0,len(tree_tag), 4):
#    print(i)
#    print(tree_tag[0:i+3])
#    a = (tree_tag[0:i+3])

#k = id_name_tree_df.Id[id_name_tree_df.Id == 'D000039'].index.tolist()
#print(k)
#
#id_name_tree_df['Id'].where(tree_tag2 in id_name_tree_df['TreeNumbers'])
#
#k = id_name_tree_df.Id[tree_tag2 in id_name_tree_df['TreeNumbers']].index.tolist()
#
#k = (id_name_tree_df.TreeNumbers[id_name_tree_df.TreeNumbers])
#
#a = id_name_tree_df['TreeNumbers']
#for i in range(0,len(a)):
#    if tree_tag2 in a[i]:
#        print('True')
        
a = id_name_tree_df['TreeNumbers']
for index, item in enumerate(a):
    if tree_tag4 in item:
        print(index, 'True')
        print(id_name_tree_df.loc[index,'Id'])
        print(id_name_tree_df.loc[index,'Name'])
        
        
#k = (id_name_tree_df.TreeNumbers[id_name_tree_df.TreeNumbers == tree_tag_list].index.tolist())
#print(k)

    
    
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







