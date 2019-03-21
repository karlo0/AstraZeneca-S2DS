#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Begun on Mon Mar 18 14:30:13 2019

@author: nLp ATTACK
"""

import pandas as pd
import pickle

# initialize
id_name_tree_df = pd.DataFrame([], columns=['Id','Name', 'TreeNumbers'])
id_name_tree_dict = {}
tree_value = []

with open('../data/external/d2019.txt') as f:    
    for line in f: # cycle through each line
        if line.startswith('MH = '): # name
            id_name_tree_dict['Name'] = line[5:-1]
        
        if line.startswith('MN = '): # tree numbers
            # collect tree number for each line            
            tree_value_temp = line[5:] 
            # include last char \n because it will help to search each level of the tree
            # collect all tree numbers
            tree_value.append(tree_value_temp)
            
        id_name_tree_dict['TreeNumbers'] = tree_value       
               
        if line.startswith('UI = '): # unique id
            tree_value = [] # initialize since all tree numbers are obtained
            id_name_tree_dict['Id'] = line[5:-1]
            id_name_tree_df = id_name_tree_df.append(id_name_tree_dict, ignore_index=True)            

id_name_tree_df.to_pickle('../data/processed/id_name_tree.pkl')
