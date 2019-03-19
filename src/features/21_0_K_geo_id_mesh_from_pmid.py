import numpy as np
import pandas as pd
import pickle
from Bio import Entrez
Entrez.email = "karsten.leonhardt@posteo.de"
try:
    from urllib.error import HTTPError  # for Python 3
except ImportError:
    from urllib2 import HTTPError  # for Python 2

l_data_dir = "../../data/local_data/data_records_and_sample/"

def import_geo_df():
    # comment out one of the two follwing
    # fname = "samples.pkl"
    fname = "records.pkl"
    print("start load geo database")
    df = pickle.load( open(l_data_dir+fname, 'rb') )
    print("done")
    return df

#keys of the dataframe:
# ['Id', 'nsamples', 'Accession', 'ExtRelations', 'FTPLink', 'GDS',
# 'GEO2R', 'GPL', 'GSE', 'Item', 'PDAT', 'PlatformTaxa', 'PlatformTitle',
# 'Projects', 'PubMedIds', 'Relations', 'SSInfo', 'Samples',
# 'SamplesTaxa', 'SeriesTitle', 'entryType', 'gdsType', 'n_samples',
# 'ptechType', 'subsetInfo', 'summary', 'suppFile', 'taxon', 'title',
# 'valType']

geo_df = import_geo_df()

def write_mesh_to_df(geo_df):
    pmid_series = geo_df.PubMedIds

    list_geo_id = []
    list_pmid = []

    for index, row in geo_df.iterrows():
        for pmid in row['PubMedIds']:
            list_geo_id.append(row['Id'])
            list_pmid.append(str(Entrez.Parser.IntegerElement(pmid)))

    search_results = Entrez.read(Entrez.epost("pubmed", id=",".join(list_pmid)))
    webenv = search_results["WebEnv"]
    query_key = search_results["QueryKey"]

    count = len(list_pmid)
    # count = 10
    batch_size = 1000

    # initialize global lists for pmid number, mesh tag, mesh ui and the mesh flag whether it is major topic or not 
    list_pmid_unique = []
    list_mesh_tag = []
    list_mesh_ui = []
    list_mesh_maj_topic = []
    # start iterating over batch_size samples to fetch from pubmed
    for start in range(0, count, batch_size):
        if batch_size == 1:
            end = start
        else:
            end = min(count, start + batch_size)
        print("Going to download record %i to %i" % (start+1, end))
        attempt = 1
        not_fetched = True
        while ((attempt <= 3) and not_fetched):
            try:
                fetch_handle = Entrez.efetch(db="pubmed", retstart=start, retmax=min(10000, batch_size), retmode="xml", webenv=webenv, query_key=query_key)
                data = Entrez.read(fetch_handle)
                
                for pm_artcle in data['PubmedArticle']:
                    pmid = Entrez.Parser.StringElement(pm_artcle['MedlineCitation']['PMID'])
                    if pmid not in list_pmid_unique:
                        list_pmid_unique.append(pmid)
                        # initialize local lists for the mesh tag, ui and the flag whether it is major topic or not 
                        list_mesh_tag_local = []
                        list_mesh_ui_local = []
                        list_mesh_maj_topic_local = []
                        # enter the list of mesh entries
                        try:
                            list_mesh = pm_artcle['MedlineCitation']['MeshHeadingList']
                            for mesh_entry in list_mesh:
                                mesh = mesh_entry['DescriptorName']
                                mesh_attr = mesh.attributes
                                mesh_tag = mesh[:]
                                mesh_ui = mesh_attr['UI']
                                mesh_maj_topic = mesh_attr['MajorTopicYN']
                                list_mesh_ui_local.append(mesh_ui)
                                list_mesh_tag_local.append(mesh_tag)
                                if mesh_maj_topic == 'N':
                                    list_mesh_maj_topic_local.append(False)
                                else:
                                    list_mesh_maj_topic_local.append(True)
                        except KeyError:
                            pass
                        list_mesh_tag.append(list_mesh_tag_local)
                        list_mesh_ui.append(list_mesh_ui_local)
                        list_mesh_maj_topic.append(list_mesh_maj_topic_local)

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

    list_pmid_unique       = np.array(list_pmid_unique)
    list_mesh_tag          = np.array(list_mesh_tag)
    list_mesh_ui           = np.array(list_mesh_ui)
    list_mesh_maj_topic    = np.array(list_mesh_maj_topic)

    list_geo_id_unique         = []
    list_mesh_tag_unique       = []
    list_mesh_ui_unique        = []
    list_mesh_maj_topic_unique = []

    geo_id_old = ''
    for k in range(count):
        geo_id = list_geo_id[k]
        pmid = list_pmid[k]
        bool_ar = list_pmid_unique == pmid
        print(k)
        if geo_id != geo_id_old:
            if k > 0:
                list_geo_id_unique.append(geo_id_old)
                list_mesh_tag_unique.append(list_mesh_tag_local )
                list_mesh_ui_unique.append(list_mesh_ui_local )
                list_mesh_maj_topic_unique.append(list_mesh_maj_topic_local)

            list_mesh_tag_local         = list_mesh_tag[bool_ar][0]
            list_mesh_ui_local          = list_mesh_ui[bool_ar][0]
            list_mesh_maj_topic_local   = list_mesh_maj_topic[bool_ar][0]
        else:
            np_list_mesh_tag_tmp = np.array(list_mesh_tag[bool_ar][0])
            np_list_mesh_ui_tmp = np.array(list_mesh_ui[bool_ar][0])
            np_list_mesh_maj_topic_tmp = np.array(list_mesh_maj_topic[bool_ar][0])
            for mesh_ui in np_list_mesh_ui_tmp:
                if mesh_ui not in list_mesh_ui_local:
                    bool_ar_tmp = np_list_mesh_ui_tmp == mesh_ui
                    list_mesh_ui_local.append(mesh_ui)
                    list_mesh_tag_local.append(np_list_mesh_tag_tmp[bool_ar_tmp][0])
                    list_mesh_maj_topic_local.append(np_list_mesh_maj_topic_tmp[bool_ar_tmp][0])
        geo_id_old = geo_id

    list_geo_id_unique.append(geo_id_old)
    list_mesh_tag_unique.append(list_mesh_tag_local )
    list_mesh_ui_unique.append(list_mesh_ui_local )
    list_mesh_maj_topic_unique.append(list_mesh_maj_topic_local)

    df_geo_pmid_mesh = pd.DataFrame({'Id': np.array(list_geo_id_unique), 'mesh_tags': np.array(list_mesh_tag_unique), 'mesh_uis': np.array(list_mesh_ui_unique), 'mesh_maj_topics': np.array(list_mesh_maj_topic_unique)})

    return df_geo_pmid_mesh

df_geo_pmid_mesh = write_mesh_to_df(geo_df)

# write dataframe to file
df_geo_pmid_mesh.to_pickle("./geo_id_mesh_from_pmid.pkl")
