#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Begun on Mon Mar 18 14:30:13 2019

@author: nLp ATTACK

"""

def match_mesh_disease_id_to_disease_hierarchy(diseases_vocab_df, mesh_id):
    for index, row in diseases_vocab_df["DiseaseID"].iteritems():
        if mesh_id in row:
            disease_name = diseases_vocab_df.loc[index, "DiseaseName"]
            disease_hierarchy_temp = diseases_vocab_df.loc[index, "SlimMappings"]
            disease_hierarchy = [];
            index1 = 0
            for index2, character in enumerate(disease_hierarchy_temp):
                if character == '|':
                    disease_hierarchy.append(disease_hierarchy_temp[index1:index2])
                    index1 = index2+1
            disease_hierarchy.append(disease_hierarchy_temp[index1:])
            disease_hierarchy.reverse()
            disease_hierarchy.append(disease_name)
            
            return True, index, disease_name, disease_hierarchy
    return False

import pandas as pd
ctd_diseases_df = pd.read_csv('CTD_diseases.csv')

(value, index, disease_name, disease_hierarchy) = match_mesh_disease_id_to_disease_hierarchy(ctd_diseases_df, 'D020388')

print(disease_hierarchy)





