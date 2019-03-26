import pickle
from Bio import Entrez
import pandas as pd
import numpy as np
Entrez.email = "karsten.leonhardt@posteo.de"


dir_data_in = "../../data/interim/"
dir_data_out = "../../data/final/"

def import_df_records():
    fname = "records.pkl"
    print("start load geo database")
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

def import_meshid_name_tree():
    fname = "id_name_tree_with_SCR.pkl"
    print("start load df with id name tree including SCR to name")
    df = pickle.load( open(dir_data_in+fname, 'rb') )
    print("done")
    return df

df_records = import_df_records()
df_meshid_name= import_meshid_name_tree()
# remove the \n in the treenumbers of Arun's df
df_meshid_name['TreeNumbers'] = df_meshid_name['TreeNumbers'].apply(lambda x: [x_el.replace('\n','') for x_el in x])
# rename columns of Arun's df
df_meshid_name = df_meshid_name.rename(index=str, columns={'Id': 'mesh_id', 'Name': 'mesh_heading', 'TreeNumbers': 'mesh_treenumbers'})

df_geoid_tags_dnorm = import_arrange_df_tags_from_dnorm()
df_geoid_mesh_pmid = import_arrange_df_tags_from_pmid()

df = pd.concat([df_geoid_tags_dnorm, df_geoid_mesh_pmid], ignore_index=True)

df = df.drop_duplicates()
df = df.sort_values(by=['geo_id']).reset_index(drop = True)

df_tmp = df_records[['Id', 'nsamples']]
df_tmp = df_tmp.set_index('Id').T
df_tmp = df_tmp[df['geo_id'].values]
df['nsamples'] = pd.Series(data = df_tmp.loc['nsamples'].values, index = df.index)

del df_tmp

df = df[['geo_id', 'nsamples', 'date', 'mesh_id']]

mesh_ids_intersect = np.intersect1d(np.unique(df['mesh_id'].values), df_meshid_name['mesh_id'])

df = df[df['mesh_id'].isin(mesh_ids_intersect)]

def eval_treenumbers(x):
    if len(x) == 0:
        return 'Sex'
    else:
        return x[0][0]

df_tmp = df_meshid_name[['mesh_id', 'mesh_treenumbers']]
df_tmp['mesh_treenumbers'] = df_tmp['mesh_treenumbers'].apply(lambda x: eval_treenumbers(x))
df_tmp = df_tmp.set_index('mesh_id').T
df_tmp = df_tmp[df['mesh_id'].values]
df['category'] = pd.Series(data = df_tmp.loc['mesh_treenumbers'].values, index = df.index)

print("store dfs")
df.to_pickle(dir_data_out+"df_geoid_meshid__no_omim_scr.pkl")
df_meshid_name.to_pickle(dir_data_out+"df_mesh__id_heading_treenumber_v1.pkl")
