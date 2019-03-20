#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Begun on Mon Mar 18 14:30:13 2019

@author: nLp ATTACK

"""
import pandas as pd

id_name = pd.DataFrame([], columns=['DiseaseId','DiseaseName'])

id_hierarchy_dict = {}

with open('../data/external/d2019_expt.txt') as f:
    #content = f.readline()
    for line in f:
        if line.startswith('MH = '):
            id_hierarchy_dict['DiseaseName'] = line[5:-1]
#        if line.startswith('MN = '):
#            value2_temp = line[5:-1]
#            print(value)
#            value2 = []
#            value2.append(value2_temp)
        if line.startswith('UI = '):
            id_hierarchy_dict['DiseaseId'] = line[5:-1]          
            id_name = id_name.append(id_hierarchy_dict, ignore_index=True)            

print(id_name)




#
#import pandas as pd
#
#df = pd.DataFrame(disease_hierarchy)
#print(df)





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







