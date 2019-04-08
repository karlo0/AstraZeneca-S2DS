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

# Read samples data
samples_df = pd.read_pickle('../../data/interim/samples.pkl')

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
        
geo_id_samples = samples_df.loc[samples_df['geo_id'] == '200003505']
sample_titles = list(geo_id_samples.title)
start_time = time.time() # to monitor time taken
cluster_terms(sample_titles)
end_time = time.time() # to monitor time taken
print('\ntime taken: ', end_time - start_time, 'seconds')