import numpy as np
import pandas as pd
import pickle

def import_df_geo_pmid_mesh():
    # comment out one of the two follwing
    fname = "geo_id_mesh_from_pmid.pkl"
    print("start load geo-pmid-mesh database")
    l_data_dir = "../../data/interim/"
    df = pickle.load( open(l_data_dir+fname, 'rb') )
    print("done")
    return df

def import_geo_df():
    # comment out one of the two follwing
    # fname = "samples.pkl"
    fname = "records.pkl"
    print("start load geo database")
    l_data_dir = "../../data/local_data/data_records_and_sample/"
    df = pickle.load( open(l_data_dir+fname, 'rb') )
    print("done")
    return df

geo_df = import_geo_df()
df_geo_pmid_mesh = import_df_geo_pmid_mesh()

def add_date_to_df(df_geo_pmid_mesh, geo_df):
    print('add date column to dataframe')
    df_tmp = geo_df[['Id', 'PDAT']]
    df_tmp = df_tmp.set_index('Id').T
    df_tmp = df_tmp[df_geo_pmid_mesh['Id'].values]
    df_geo_pmid_mesh['date'] = pd.Series(data = df_tmp.loc['PDAT'].values, index = df_geo_pmid_mesh.index)
    return df_geo_pmid_mesh

def finalize_df_geo_pmid_mesh(df_geo_pmid_mesh, geo_df):
    print('finalize dataframe')
    df_tmp = add_date_to_df(df_geo_pmid_mesh, geo_df)
    df = df_tmp['mesh_uis'].apply(pd.Series)
    df = df.rename(columns = lambda x: 'tmp_' + str(x))
    df['geo_id'] = df_tmp['Id']
    df['date'] = df_tmp['date']
    tmp_column_names = df.columns
    df = df.melt(id_vars=['geo_id', 'date'])
    df = df.drop(columns = 'variable')
    df = df.rename(columns={'value': 'mesh_id'})
    df = df[~df.mesh_id.isnull()]
    df = df.sort_values(by=['geo_id']).reset_index(drop = True)
    return df

def list_to_np_and_flatten(vec):
    return np.hstack(np.array(list(map(lambda x: np.array(x), vec))))

def extract_mesh_tags_uis(df_geo_pmid_mesh):
    print('extract mesh_tags and mesh uis')
    mesh_tags = df_geo_pmid_mesh['mesh_tags'].values
    mesh_uis = df_geo_pmid_mesh['mesh_uis'].values

    mesh_tags   =  np.unique(list_to_np_and_flatten(mesh_tags))
    mesh_uis    =  np.unique(list_to_np_and_flatten(mesh_uis))

    return pd.DataFrame({'mesh_id': mesh_uis, 'mesh_word': mesh_tags})

df_mesh_ui_tags = extract_mesh_tags_uis(df_geo_pmid_mesh)

print('store dataframe for mesh uis and words')
df_mesh_ui_tags.to_pickle("../../data/interim/df_mesh_ui_words.pkl")

df_geoid_date_meshui_from_pmid = finalize_df_geo_pmid_mesh(df_geo_pmid_mesh, geo_df)

print('store dataframe for geoid-date-meshui relation')
df_geoid_date_meshui_from_pmid.to_pickle("../../data/interim/df_geoid_date_meshui_from_pmid.pkl")
