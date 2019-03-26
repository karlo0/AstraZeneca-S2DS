"""Script to use the in a pandas df stored data of all geo series and retrieve mesh headings and mesh ids for them via following linked pubmed publications"""
import numpy as np
import pandas as pd
import pickle
import os
from Bio import Entrez
Entrez.email = "A.N.Other@example.com" # Always tell NCBI who you are
try:
    from urllib.error import HTTPError  # for Python 3
except ImportError:
    from urllib2 import HTTPError  # for Python 2

dir_data_in = "../../data/interim/records_samples/"

project_name = "AstraZenecaMar19"

output_data_path = '../../data/interim/'
fname = "df_geoid_date_meshui_from_pmid.pkl"

fpath = os.path.realpath(__file__)
commonpath = os.path.commonpath([fpath, project_name])

def import_df_records():
    fname = "records.pkl"
    print("start load records database")
    df = pickle.load( open(dir_data_in+fname, 'rb') )
    print("done")
    return df

#keys of the dataframe:
# ['Id', 'nsamples', 'Accession', 'ExtRelations', 'FTPLink', 'GDS',
# 'GEO2R', 'GPL', 'GSE', 'Item', 'PDAT', 'PlatformTaxa', 'PlatformTitle',
# 'Projects', 'PubMedIds', 'Relations', 'SSInfo', 
# 'SamplesTaxa', 'SeriesTitle', 'entryType', 'gdsType', 'n_samples',
# 'ptechType', 'subsetInfo', 'summary', 'suppFile', 'taxon', 'title',
# 'valType']

# import records dataframe
df_records = import_df_records()

def write_mesh_to_df(df_records):
    pmid_series = df_records.PubMedIds

    list_pmid_unique = []

    #filter all unique pubmed ids

    pmid_series_tolist = df_records['PubMedIds'].apply(lambda x: x.tolist())
    df_records = df_records[pmid_series_tolist != 2*pmid_series_tolist].reset_index(drop=True)

    list_pmid_unique = np.unique(np.hstack(df_records['PubMedIds'].values))

    search_results = Entrez.read(Entrez.epost("pubmed", id=",".join([str(x) for x in list_pmid_unique])))


    webenv = search_results["WebEnv"]
    query_key = search_results["QueryKey"]

    count = len(list_pmid_unique)
    batch_size = 1000

    # initialize global dict for all distinct pmid numbers and their corresponding lists of mesh-ui numbers
    dict_pmid_mui = {x: [] for x in list_pmid_unique}

    # start iterating over batch_size samples to fetch from pubmed
    for start in range(0, count, batch_size):
        if batch_size == 1:
            end = start
        else:
            end = min(count, start + batch_size)
        print("Going to download mesh-ui numbers of the pubmed puplications %i to %i" % (start+1, end))
        attempt = 1
        not_fetched = True
        while ((attempt <= 3) and not_fetched):
            try:
                fetch_handle = Entrez.efetch(db="pubmed", retstart=start, retmax=min(10000, batch_size), retmode="xml", webenv=webenv, query_key=query_key)
                data = Entrez.read(fetch_handle)
                
                for pm_artcle in data['PubmedArticle']:
                    pmid = np.int64(Entrez.Parser.StringElement(pm_artcle['MedlineCitation']['PMID']))
                    # initialize local lists for the mesh tag, ui and the flag whether it is major topic or not 
                    list_mui_local = []
                    # enter the list of mesh entries
                    try:
                        list_mesh = pm_artcle['MedlineCitation']['MeshHeadingList']
                        for mesh_entry in list_mesh:
                            mesh = mesh_entry['DescriptorName']
                            mesh_attr = mesh.attributes
                            mesh_ui = mesh_attr['UI']
                            list_mui_local.append(mesh_ui)
                        if len(list_mui_local) > 0:
                            dict_pmid_mui[pmid] = list_mui_local
                    except KeyError:
                        pass

                fetch_handle.close()
                not_fetched = False
            except HTTPError as err:
                not_fetched = True
                if 500 <= err.code <= 599:
                    print("Received error from server %s" % err)
                    print("Attempt %i of 3" % attempt)
                    attempt += 1
                    time.sleep(3)
                else:
                    raise

    list_geoid_global           = []
    list_geoid_nsamples_global  = []
    list_geoid_date_global      = []
    list_geoid_mui_global       = []

    for k in df_records.index:

        list_geoid_mui_local = []
        list_geoid_pmid_local = df_records['PubMedIds'].iloc[k]

        if list_geoid_pmid_local.size != 0:
            for pmid in list_geoid_pmid_local:
                list_geoid_mui_local.extend(dict_pmid_mui[pmid])

            list_geoid_mui_local = list(set(list_geoid_mui_local))
            len_list_geoid_mui_local = len(list_geoid_mui_local)
            if len_list_geoid_mui_local > 0:
                geoid = df_records['Id'].iloc[k]
                n_samples = df_records['n_samples'].iloc[k]
                date = df_records['PDAT'].iloc[k]

                list_geoid_global.extend(len_list_geoid_mui_local*[geoid])
                list_geoid_nsamples_global.extend(len_list_geoid_mui_local*[n_samples])
                list_geoid_date_global.extend(len_list_geoid_mui_local*[date])
                list_geoid_mui_global.extend(list_geoid_mui_local)


    df_geoid_mesh_pmid= pd.DataFrame({'geo_id': np.array(list_geoid_global), 'nsamples': np.array(list_geoid_nsamples_global), 'date': np.array(list_geoid_date_global), 'mesh_id': np.array(list_geoid_mui_global)})

    return df_geoid_mesh_pmid

df_geoid_mesh_pmid = write_mesh_to_df(df_records)

df_geoid_mesh_pmid = df_geoid_mesh_pmid[['geo_id', 'nsamples', 'date', 'mesh_id']].sort_values(by=['geo_id']).reset_index(drop = True)

#write dataframe to file
df_geoid_mesh_pmid.to_pickle(output_data_path+fname)
