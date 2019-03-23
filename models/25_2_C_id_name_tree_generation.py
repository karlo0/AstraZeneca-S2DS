#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: nLp ATTACK
"""

import pandas as pd
import pickle

# initialize
id_name_tree_df = pd.DataFrame([], columns=['Id','Name', 'TreeNumbers'])
id_name_tree_dict = {}
tree_value = []

name_list = []
tree_number_list = []
id_list = []

with open('../data/external/d2019.txt') as f:
    for line in f: # cycle through each line
        
        if line.startswith('MH = '): # name
            name_list.append(line[5:-1])
        
        if line.startswith('MN = '): # tree numbers
            # collect tree number for each line            
            tree_value_temp = line[5:-1] 
            # include last char \n because it will help to search each level of the tree
            # collect all tree numbers
            tree_value.append(tree_value_temp)
               
        if line.startswith('UI = '): # unique id
            tree_number_list.append(tree_value)
            tree_value = [] # initialize since all tree numbers are obtained
            id_list.append(line[5:-1])
        
df = pd.DataFrame.from_dict({'mesh_id':pd.Series(id_list),'mesh_heading':pd.Series(name_list), 'mesh_treenumbers':pd.Series(tree_number_list)})     

# turn list into columns
# expand list into columns
tags = df.mesh_treenumbers.apply(pd.Series)
cols = ['tag'+str(icol) for icol in tags.columns]
tags.columns = cols
tags['mesh_id'] = df.mesh_id
df = pd.merge(df,tags, on='mesh_id', how='inner')
# melt
df = pd.melt(df, id_vars = ['mesh_id','mesh_heading'], value_vars=cols)
df = df.drop('variable',axis=1)
df.columns = ['mesh_id','mesh_heading', 'mesh_treenumbers']
df['category'] = df.mesh_treenumbers.str[:1]
df = df.dropna()

df.to_pickle('../data/processed/id_name_tree.pkl')


# extra piece of code that adds levels of tree as separate columns
# (Claire: I still like the levels in columns because it should work well with pandas :) )
# for just diseases df_disease is 9MB, one column with full tree name is 5MB. We can compare speed of searching?

levels_of_tree_in_column = 0
if levels_of_tree_in_column == 1:
    df_disease = df[df.category=='C'].reset_index()
    df_disease['tag_list'] = df_disease.mesh_treenumbers.str.split('.')
    tags = df_disease['tag_list'].apply(pd.Series)
    cols = ['level'+str(icol) for icol in tags.columns]
    tags.columns = cols
    tags['level0'] = tags['level0'].str[1:]
    tags['mesh_treenumbers'] = df_disease.mesh_treenumbers
    df_disease = pd.merge(df_disease,tags, on='mesh_treenumbers', how='inner')
    df_disease = df_disease.drop('tag_list', axis=1)