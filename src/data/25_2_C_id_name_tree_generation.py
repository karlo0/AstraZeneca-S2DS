#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: nLp ATTACK

# This code downloads tree IDs and supplemental concept records (SCRs) and puts them into one df
# file from here: ftp://nlmpubs.nlm.nih.gov/online/mesh/MESH_FILES/asciimesh/ 

# output df columns are: 
# 'category': record type (eg disease='C')
# 'mesh_id': unique id (UI) given to record (eg, D013614)
# 'mesh_heading': concept name (eg, 'Adams Nance syndrome')
# 'mesh_treenumbers': address in tree, with sub categories separated by '.' 
# (eg C14.280.067.845.695), one concept can have many mesh_treenumbers
# 'scr': is this a supplemental concept record. 0 for no, 1 for yes. There are ~600K SCRs and ~50K MeSH records


# SCRs Supplemental concept records:
# more info: search MeSH here https://meshb.nlm.nih.gov/search and more info here https://www.nlm.nih.gov/mesh/intro_record_types.html
# Fields of SCR file:
# The names (NM) are new concepts
# the NMs map to certain concepts that are already in the MeSH (HM)
# The SCRs have their own unique identifiers UIs as well

# How can we deal with SCR?
# These new concepts might be tags of Karsten's PMID data for example
# We can map the new record names NMs to existing MeSH ids (UIs and tree IDs) 
# -- this is the only way of linking this data with the tree. Then we search SCRs as if they were mesh headings
# result: in our use case, we can search the tags for disease names, including SCR names

"""

import pandas as pd
import pickle

# initialize
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


new_name_list = []
maps_to = []
maps_to_list = []
id_list = []

with open('../data/external/c2019.txt') as f:
    for line in f: # cycle through each line
        
        if line.startswith('NM = '): # new name
            new_name_list.append(line[5:-1])
        
        if line.startswith('HM = '): # maps to names in MeSH           
            maps_to_temp = line[5:-1].split('/')[0].replace('*','')
            maps_to.append(maps_to_temp)
               
        if line.startswith('UI = '): # unique id
            maps_to_list.append(maps_to)
            maps_to = [] # initialize since all tree numbers are obtained
            id_list.append(line[5:-1])
        
scr_df = pd.DataFrame.from_dict({'SCR_id':pd.Series(id_list),'SCR_name':pd.Series(new_name_list),'mesh_heading':pd.Series(maps_to_list)})     
# expand list into columns, then melt
tags = scr_df.mesh_heading.apply(pd.Series)
cols = ['tag'+str(icol) for icol in tags.columns]
tags.columns = cols
tags['SCR_id'] = scr_df.SCR_id
scr_df = pd.merge(scr_df,tags, on='SCR_id', how='inner')
scr_df = pd.melt(scr_df, id_vars = ['SCR_id','SCR_name'], value_vars=cols)
scr_df = scr_df.drop('variable',axis=1)
scr_df.columns = ['SCR_id','SCR_name', 'mesh_heading']
scr_df = scr_df.dropna()

# SCR_name becomes new mesh_heading so we can search directly for the SCRs, then add to main df
scr_df = pd.merge(scr_df[['SCR_name', 'mesh_heading']], df, on='mesh_heading', how='inner')
scr_df = scr_df.drop('mesh_heading', axis = 1)
scr_df = scr_df.rename(index=str, columns = {'SCR_name':'mesh_heading'})
scr_df['scr'] = 1

df['scr'] = 0

df = pd.concat([df, scr_df], ignore_index=True)

df.to_pickle('../data/processed/id_name_tree.pkl')


# extra piece of code: 
# This turns the tree address into columns. gives indexing that should work well with pandas. downside: larger file
# for just diseases with scr, df_disease is 9MB, one column with full tree name is 5MB. 
# We could compare speed of searching with full address and separate columns, in case it's faster?

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