import pickle
from Bio import Entrez
import pandas as pd
import numpy as np
import os
Entrez.email = "karsten.leonhardt@posteo.de"

# decide whether to load mesh df with (=1) or without (=0) SCFs
include_SCR = 0

## Set paths
# cdir = dir of this script
cdir = os.path.dirname(os.path.realpath(__file__))
# basedir = root dir of the repository
basedir = os.path.dirname(os.path.dirname(cdir))


dir_data_in = basedir+"/data/interim/"
dir_data_out = basedir+"/data/final/"

def import_df_records():
    fname = "records.pkl"
    print("start load raw geo dataframe")
    records_samples_folder = "records_samples/"
    df = pickle.load( open(dir_data_in+records_samples_folder+fname, 'rb') )
    print("done")
    return df

def import_arrange_df_tags_from_dnorm():
    fname = "disease_tags_dnorm_advanced.pkl"
    print("start load df with mesh data obtained via DNORM")
    df = pickle.load( open(dir_data_in+fname, 'rb') )
    df = df[df['ont'] == 'MESH']
    df = df.drop(columns=['start','end', 'disease_tag', 'tag_type', 'ont'])
    df = df.rename(index=str, columns={'Id': 'geo_id', 'PDAT': 'date', 'unique_id': 'mesh_id'})
    df['geo_id'] = df['geo_id'].apply(lambda x: str(x))
    df['date'] = df['date'].apply(lambda x: str(x))
    df = df.drop_duplicates()
    print("done")
    return df

def import_arrange_df_tags_from_pmid():
    fname = "df_geoid_date_meshui_from_pmid.pkl"
    print("start load df with mesh data obtained via following pubmed publications")
    df = pickle.load( open(dir_data_in+fname, 'rb') )
    print("done")
    return df

def import_df_mesh():
    fname = 'mesh_wSCR.pkl'
    print("start load mesh df with meshid-mesh headings-mesh tree number rows")
    df = pickle.load( open(dir_data_out+fname, 'rb') )
    print("done")
    return df


df_records = import_df_records()
df_mesh= import_df_mesh()

df_geoid_tags_dnorm = import_arrange_df_tags_from_dnorm()
df_geoid_mesh_pmid = import_arrange_df_tags_from_pmid()

df_geoid_tags_dnorm['method'] = 'dnorm'
df_geoid_mesh_pmid['method'] = 'pmid'

# add back the nsamples column from the records df
df_geoid_tags_dnorm = pd.merge(df_geoid_tags_dnorm, df_records[['Id', 'n_samples']], left_on = 'geo_id', right_on = 'Id', how = 'left')

df_geoid_tags_dnorm = df_geoid_tags_dnorm.rename(index=str, columns={'n_samples': 'nsamples'})

df_geoid_tags_dnorm = df_geoid_tags_dnorm[['geo_id', 'nsamples', 'date', 'mesh_id', 'method']]
df_geoid_mesh_pmid = df_geoid_mesh_pmid[['geo_id', 'nsamples', 'date', 'mesh_id', 'method']]

# concat both dataframes
df = pd.concat([df_geoid_tags_dnorm, df_geoid_mesh_pmid], ignore_index=True)


df = df.drop_duplicates(subset=list(df_geoid_tags_dnorm.columns[0:-1]))


df = pd.merge(df, df_mesh[['category', 'mesh_heading', 'mesh_id']].drop_duplicates(), on='mesh_id', how='left')

df = df[['geo_id', 'nsamples', 'date', 'mesh_id', 'mesh_heading', 'category', 'method']]


df = df.sort_values(by=['geo_id']).reset_index(drop = True)

print("store geo df")
df.to_pickle(dir_data_out+"geo.pkl")
