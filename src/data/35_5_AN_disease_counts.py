#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Begun on Wed Mar 18 14:30:13 2019

@author: nLp ATTACK

gives a count of the diseases mentioned as mesh ids in the geoseries data for 
homo sapiens, extracted and saved in geo.pkl

uses mesh hierarchy as given in https://meshb.nlm.nih.gov/treeView, which was 
extracted and saved in mesh.pkl

the count is obtained and saved as a pkl file 'disease_mesh_heading_count.pkl'
that consists of a pandas dataframe 'diseases_count_df' with two columns:
    'disease_mesh_heading', 'disease_count'

the counting algorithm is as follows:    
(1) geo.pkl is the input and mesh.pkl is the input vocablary
(2) write two functions to
    (1) convert any mesh_id to all its tree numbers using mesh.pkl
    (2) take a treenumber and convert it into its parent tree hierarchy of mesh_headings.
(3) iterate over every study in geo.pkl
    (1) find all the mesh-ids of the study (e.g., male breast cancer C02.001.001)
    (2) for each mesh-id, find its tree ids and parents (e.g., breast cancer = C02.001 and cancer = C02)
    (3) collect all the parents for all mesh-ids and make the set of parents unique
    (4) update counts for parents and the disease (e.g., male breast cancer, breast cancer, and cancer)    
(4) collect the counts and export
"""
import pandas as pd
import time
start_time = time.time()

# read the mesh database pkl file
mesh_df = pd.read_pickle('../../data/final/mesh.pkl')

## define two required functions
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

## start the counting
    
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

diseases_count_df = pd.DataFrame(disease_count.items())
diseases_count_df = pd.DataFrame(disease_count.items(), columns = ['disease_mesh_heading', 'disease_count'])
diseases_count_df.to_pickle('../../data/processed/disease_mesh_heading_count.pkl')

end_time = time.time()
print("total time taken:", start_time-end_time)

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