#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 12:39:16 2019

@author: arun
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#print(all_hierarchies)
from PIL import Image
#import WordCloud
#import matplotlib.pyplot as plt
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

print(convert_meshid_to_tree_numbers('D016000'))
