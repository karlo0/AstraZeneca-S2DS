#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 14:40:07 2019

@author: arun
"""

import pandas as pd
import numpy as np
import sklearn.cluster
import distance # first, >>> pip install Distance
import time
import itertools

## Define required functions

# function for clustering using levenshtein distance and affinity propagation
def cluster_terms(input_words):
    """
    list of word strings --> prints exemplar_str, cluster_str
    """
    words = np.asarray(input_words) #So that indexing with a list will work
    lev_similarity = -1*np.array([[distance.levenshtein(w1,w2) for w1 in words] for w2 in words])

    affprop = sklearn.cluster.AffinityPropagation(affinity="precomputed", damping=0.5)
    affprop.fit(lev_similarity)
    for cluster_id in np.unique(affprop.labels_):
        exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
        cluster = np.unique(words[np.nonzero(affprop.labels_==cluster_id)])
        cluster_str = ", ".join(cluster)
        print(" - *%s:* %s" % (exemplar, cluster_str))
        

# Read samples data
samples_df = pd.read_pickle('../../data/interim/samples.pkl')
        
geo_id_samples = samples_df.loc[samples_df['geo_id'] == '200003505']
sample_titles = list(geo_id_samples.title)
start_time = time.time() # to monitor time taken
cluster_terms(sample_titles)
end_time = time.time() # to monitor time taken
print('\ntime taken: ', end_time - start_time, 'seconds')

#def long_substr(data):
#    substr = ''
#    if len(data) > 1 and len(data[0]) > 0:
#        for i in range(len(data[0])):
#            for j in range(len(data[0])-i+1):
#                if j > len(substr) and is_substr(data[0][i:i+j], data):
#                    substr = data[0][i:i+j]
#    return substr
#
#def is_substr(find, data):
#    if len(data) < 1 and len(find) < 1:
#        return False
#    for i in range(len(data)):
#        if find not in data[i]:
#            return False
#    return True
#
#text = ['WTCHG_380869_201250: M38+ Gut single cell', 'WTCHG_380869_201251: M38+ Gut single cell', 'WTCHG_380869_202250: M38+ Gut single cell', 'WTCHG_380869_202251: M38+ Gut single cell', 'WTCHG_380869_203251: M38+ Gut single cell bulk', 'WTCHG_380869_204250: M38+ Gut single cell', 'WTCHG_380869_204251: M38+ Gut single cell', 'WTCHG_380869_204254: M38+ Gut single cell', 'WTCHG_380869_204255: M38+ Gut single cell', 'WTCHG_380869_205251: M38+ Gut single cell', 'WTCHG_380869_206251: M38+ Gut single cell', 'WTCHG_380869_207251: M38+ Gut single cell', 'WTCHG_380869_207255: M38+ Gut single cell', 'WTCHG_380869_208251: M38+ Gut single cell', 'WTCHG_380869_208255: M38+ Gut single cell']
#text = ['A07RM 24 h PEP005', 'D04 24 h PEP005', 'D23 24 h PEP005', 'D24 24 h PEP005', 'LSPM2 24 h PEP005', 'MM127 24 h PEP005', 'MM253 24 h PEP005', 'MM455 24 h PEP005']
#print(long_substr(text))
