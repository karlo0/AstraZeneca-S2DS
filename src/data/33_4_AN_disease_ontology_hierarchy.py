#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Begun on Wed Mar 18 14:30:13 2019

@author: nLp ATTACK

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS

mesh_df = pd.read_pickle('../../data/final/mesh.pkl') # read the mesh database pkl file

def convert_meshid_to_tree_numbers(mesh_id):
    """
    converts any mesh_id to all its tree numbers using the mesh database (mesh.pkl)
    str -> list
    Examples:        
        >>> convert_meshid_to_tree_numbers('D000013')
        >>> ['C16.131']
        
        >>> convert_meshid_to_tree_numbers('D000001')
        >>> ['D03.633.100.221.173']
        
        >>> convert_meshid_to_tree_numbers('D000002')
        >>> ['D02.705.400.625.800', 'D02.705.539.345.800', 'D02.886.300.692.800']
              
        >>> convert_meshid_to_tree_numbers('D000012')
        >>> ['C16.320.565.398.500.440.500', 'C18.452.584.500.875.440.500', 'C18.452.648.398.500.440.500']
        
        >>> convert_meshid_to_tree_numbers('D000016')
        >>> ['C16.131.080', 'C26.733.031', 'G01.750.748.500.031', 'N06.850.460.350.850.500.031', 'N06.850.810.300.360.031']

        >>> convert_meshid_to_tree_numbers('D0000020')
        >>> []
        
        >>> convert_meshid_to_tree_numbers('A0000020')
        >>> []
    """
    # get the row indexes for the mesh id
    row_indexes = mesh_df.index[mesh_df['mesh_id'] == mesh_id].tolist()    
    tree_numbers = [] # initialize a list to append the tree numbers
    for row_index in row_indexes:
        tree_num = mesh_df.loc[row_index,'mesh_treenumbers']
        tree_numbers.append(tree_num)
    return tree_numbers

def convert_treenumber_to_parent_tree_hierarchy(tree_number):
    """
    takes a treenumber and converts it into its parent tree hierarchy of mesh_headings.
    the topmost mesh heading in the hierarchachy is the first entry followed by the 
    next one and so on till the mesh heading for the input tree number
    str -> list
    Examples:
        >>> convert_treenumber_to_tree_hierarchy('N06.850.460.350.850.500.031')
        >>> ['Environment and Public Health', 'Public Health', 'Environmental Pollution',
             'Environmental Exposure', 'Radiation Exposure', 'Radiation Injuries',
             'Abnormalities, Radiation-Induced']
        {Note: 'N06.850.460.350.850.500.031' = Abnormalities, Radiation-Induced}
        
        >>> convert_treenumber_to_tree_hierarchy('C26.733.031')
        >>> ['Wounds and Injuries', 'Radiation Injuries', 'Abnormalities, Radiation-Induced']
        
        >>> convert_treenumber_to_tree_hierarchy('C16.131')
        >>> ['Congenital, Hereditary, and Neonatal Diseases and Abnormalities', 'Congenital Abnormalities']
    
        >>> convert_treenumber_to_tree_hierarchy('C18.452.584.500.875.440.500')
        >>> ['Nutritional and Metabolic Diseases', 'Metabolic Diseases', 'Lipid Metabolism Disorders',
             'Dyslipidemias', 'Hypolipoproteinemias', 'Hypobetalipoproteinemias', 'Abetalipoproteinemia']

        >>> convert_treenumber_to_tree_hierarchy('D09.067.342.356.050')
        >>> ['Carbohydrates', 'Amino Sugars', 'Hexosamines', 'Galactosamine', 'Acetylgalactosamine']
    
    """
    # make list of parents' tree numbers
    all_parents = [];
    for i in range(0,len(tree_number), 4):
        all_parents.append((tree_number[0:i+3]))
    hierarchy_list = [];
    for parent in all_parents:                               
        row_index = mesh_df.index[mesh_df['mesh_treenumbers'] == parent].values[0]
        hierarchy_list.append(mesh_df.loc[row_index,'mesh_heading'])
    return(hierarchy_list)

# initialize dictionary for storing disease counts
# note: use entire mesh database so that diseases not studied get count of 0
mesh_diseases_df = mesh_df[mesh_df.category=='C'] # only disease category
disease_count = {}
for item in mesh_diseases_df.mesh_heading:
    disease_count[item] = 0

# read the input database
geo_df = pd.read_pickle('../../data/final/geo.pkl')
# note: one study, given by the geo_id, has multiple mesh_ids that correspond to 
# multiple categories like anatomy (A), diseases (C), chemicals and drugs (D), etc.
geo_diseases_df = geo_df[geo_df.category=='C'] # only disease category
# note: even after restricting to just the disease category, one study has multiple mesh_ids 
# because a study may be relevant to multiple diseases and therefore multiple trees

# make a unique dataframe in order to iterate the data while counting (see below)
unique_geo_diseases_df = geo_diseases_df.drop_duplicates(subset='geo_id')

# note: all the commented print commands were used to debug
counter = 0 # to check progress
for row_index, row in unique_geo_diseases_df.iterrows():    
    print(counter)
    unique_geo_id = unique_geo_diseases_df.loc[row_index,'geo_id']
#    print('\n', row_index, 'geo_id:', unique_geo_id)
    
    all_mesh_ids_row_index = geo_diseases_df.mesh_id[geo_diseases_df.geo_id==unique_geo_id]
#    print('mesh_ids for study given by geo_id:', unique_geo_id, '\n', all_mesh_ids_row_index)
    
    all_diseases_geo_id = [] # all diseases studied by the geo_id
    # associate each mesh_id with all its tree_numbers
    for mesh_id in all_mesh_ids_row_index:
        all_tree_numbers_mesh_id = convert_meshid_to_tree_numbers(mesh_id)
        # note: each mesh-id may have multiple tree numbers!
#        print('all tree numbers for mesh_id', mesh_id, '\n', all_tree_numbers_mesh_id)   
        # for each tree number, find all its parents
        for tree_number in all_tree_numbers_mesh_id: 
            if tree_number[0] == 'C': # exclude non-diseases (a second check)
                all_parents_disease = convert_treenumber_to_parent_tree_hierarchy(tree_number)
#                print('all parents for tree number', tree_number, '\n', all_parents_disease)
                # dont consider trees whose top level is 'Pathological'
                if not all_parents_disease[0].startswith('Pathological'):     
                    all_diseases_geo_id.extend(all_parents_disease)

#    print(all_diseases_geo_id)
    unique_diseases_geo_id = set(all_diseases_geo_id)
#    print(unique_diseases_geo_id)
    for disease in unique_diseases_geo_id:
        disease_count[disease] = disease_count[disease] + 1
    counter+= 1

#print(all_diseases_geo_id)
#print(s)
 
print(max(disease_count, key=disease_count.get))
from collections import Counter
print(Counter(disease_count).most_common(15))

all_disease_names = list(disease_count.keys())
all_disease_counts = list(disease_count.values())

convert_to_csv_df = pd.DataFrame({"disease_name": all_disease_names, "disease_counts": all_disease_counts})
convert_to_csv_df.to_csv("disease_name_count.csv", index=False)


# illustrate with a histogram
all_top_hierarchy_disease_counts = {
                                    'Bacterial Infections and Mycoses': 1198, 
                                    'Virus Diseases': 2098,
                                    'Parasitic Diseases': 191,
                                    'Neoplasms': 26085,
                                    'Musculoskeletal Diseases': 1660,
                                    'Digestive System Diseases': 4784,
                                    'Stomatognathic Diseases': 661,
                                    'Respiratory Tract Diseases': 2417,
                                    'Otorhinolaryngologic Diseases': 328,
                                    'Nervous System Diseases': 5282,
                                    'Eye Diseases': 847,
                                    'Male Urogenital Diseases': 2789,
                                    'Female Urogenital Diseases and Pregnancy Complications': 2867,
                                    'Hemic and Lymphatic Diseases': 4447,
                                    'Congenital, Hereditary, and Neonatal Diseases and Abnormalities': 3632,
                                    'Skin and Connective Tissue Diseases': 5551,
                                    'Nutritional and Metabolic Diseases': 2275,
                                    'Endocrine System Diseases': 2622,
                                    'Immune System Diseases': 5511,
                                    'Disorders of Environmental Origin': 2,
                                    'Animal Diseases': 982,
                                    'Pathological Conditions, Signs and Symptoms': 0,
                                    'Occupational Diseases': 59,
                                    'Chemically-Induced Disorders': 307,
                                    'Wounds and Injuries': 308
                                   }

print(Counter(all_top_hierarchy_disease_counts).most_common(25))

top_diseases = {'Neoplasms': 26085, 
                'Skin and Connective Tissue Diseases': 5551, 
                'Immune System Diseases': 5511, 
                'Nervous System Diseases': 5282, 
                'Skin Diseases': 4978, 
                'Digestive System Diseases': 4784, 
                'Hemic and Lymphatic Diseases': 4447, 
                'Carcinoma': 3992,                                
                'Others (16)': 3632+2867+2789+2622+2417+2275+2098+1660+1198+982+847+661+328+308+307+191+59+2
                }
                
#                'Respiratory Tract Diseases', 2417), ('Nutritional and Metabolic Diseases', 2275), ('Virus Diseases', 2098), ('Musculoskeletal Diseases', 1660), ('Bacterial Infections and Mycoses', 1198)

top_disease_names = list(top_diseases.keys())
top_disease_counts = list(top_diseases.values())

#labels = ['Cookies', 'Jellybean', 'Milkshake', 'Cheesecake']
#sizes = [38.4, 40.6, 20.7, 10.3]
#colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
#patches = plt.pie(top_disease_counts,  autopct='%1.1f%%')
#plt.legend(patches, top_disease_names, loc="best")
#plt.axis('equal')
#plt.tight_layout()
#plt.show()

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

labels = top_disease_names
values = top_disease_counts

trace = go.Pie(labels=labels, values=values)

py.iplot([trace], filename='basic_pie_chart')


plt.bar(top_disease_names, top_disease_counts, color='g')
plt.legend(top_disease_names,loc=2)
plt.show()

sum(all_disease_counts)
       
"""
# * = * = * = * = * = # code for Luis' graph  = * = * = * = * = * = * = * = * = #

import csv
import os

# [1] Part 1
# objective is to produce csv file with column1 = disease_tree_id and column2 = parent_tree_id
# for entire database
#pmid_df = pd.read_pickle('../../data/final/geo.pkl')
#disease_pmid_df = pmid_df[pmid_df.category=='C'] # select only diseases
## set up disease vocabulary subset df of main mesh df
disease_id_name_tree_df = id_name_tree_df[id_name_tree_df.category=='C'] # only disease category

# initialize
all_records = []
#disease_id_name_tree_df = disease_id_name_tree_df.iloc[0:3,] # only for testing
# go through the entire input data
for row_index, row in disease_id_name_tree_df.iterrows():
    # find all tree numbers corresonding to the mesh_id for that row
    # (each mesh_id may often have multiple tree numbers)
    all_tree_numbers = convert_meshid_to_tree_numbers(disease_id_name_tree_df.loc[row_index,'mesh_id'])        
    # iterate over the tree_numbers
    for tree_number in all_tree_numbers:
        if tree_number[0] == 'C': # additional check to ensure only diseases are selected
            parent_tree_number = tree_number[0:-4] # select parent tree number       
            all_records.append([tree_number, parent_tree_number]) # append to record

"""            
# [2] Part 2
      
# objective is to produce csv file with col1 = 'Tree_id', col2='Mesh headings', col3='Counts'

disease_count = {}
with open('disease_name_count.csv', 'r') as csvfile:
    readCSV = csv.reader(csvfile)
    disease_mesh_heading = []    
    for row in readCSV:
        disease_count[row[0]]=row[1]
#        disease_mesh_heading.append(row[0])
#        disease_count.append(rowp[1])
        

#print your_list
all_records_2 = []
tree_numbers = []
mesh_headings_list = []
disease_counts = []
for row_index, row in mesh_diseases_df.iterrows():
#    print(row_index)
    tree_number = (mesh_diseases_df.loc[row_index,'mesh_treenumbers'])
    mesh_heading = (mesh_diseases_df.loc[row_index,'mesh_heading'])
    disease_counts = (disease_count[mesh_diseases_df.loc[row_index,'mesh_heading']])
    all_records_2.append([tree_number, mesh_heading, disease_counts])
    
    
csv_columns = ['Diease_TreeNumber','Disease_Mesh_Heading', 'Disease_Count']
csv_data_list = all_records_2

currentPath = os.getcwd()
csv_file = "disease_tree_heading_count.csv"

WriteListToCSV(csv_file,csv_columns,csv_data_list)



def WriteListToCSV(csv_file,csv_columns,data_list):    
    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(csv_columns)
        for data in data_list:
            writer.writerow(data)    
    return            

csv_columns = ['Diease_TreeNumber','Parent_TreeNumber']
csv_data_list = all_records

currentPath = os.getcwd()
csv_file = "disease_parent.csv"

WriteListToCSV(csv_file,csv_columns,csv_data_list)

"""

"""

# * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = #
# * = * = * = * = * = * = * = * Archives * = * = * = * = * = * = * = * = * = #
# * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = * = #
    
   
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

"""