"""
This script constructs the Disease Graph
"""

# Import usual suspects
import pandas as pd
import networkx as nx

    
# Paths for input geo and mesh files
GEO_PATH = 'geo.pkl' 
MESH_PATH = 'mesh.pkl'

# Paths for output Gephi files
GEPHI_NODES = 'Gephi_Disease_Nodes.csv'
GEPHI_EDGES = 'Gephi_Disease_Edges.csv'

# Path for pickle disease/drugs Graph
DISEASE_GRAPH = 'Disease_Graph.pkl'
DRUGS_GRAPH = 'Drugs_Graph.pkl'

# Read mesh
mesh_df = pd.read_pickle(MESH_PATH)

# Read geo
tags_df = pd.read_pickle(GEO_PATH)

# Construct labels for Gephi
def get_gephi_labels(names_df):    

    # Check for None entries
    gephi_labels = names_df.dropna(axis=0)

    # Check for duplicates
    gephi_labels = gephi_labels.drop_duplicates(subset='mesh_id', keep='first')

    # Copy only id and label
    gephi_labels = gephi_labels.drop(columns='mesh_treenumbers category'.split())

    # Rename columns for gephi compatibility
    gephi_labels = gephi_labels.rename(columns={'mesh_id':'id', 'mesh_heading':'label'})

    # Return columns in correct order
    return gephi_labels['id label'.split()]


# Get labels for Gephi
gephi_labels = get_gephi_labels(mesh_df)    

# Save to .csv
gephi_labels.to_csv(GEPHI_NODES, index=False)


#
# - Construct Graph
#

# Select a subset of the data
def get_subselection(tags_df, date_l, date_h, category):

    # Construct date filter
    mask_date = ((tags_df['date']>=date_l) & (tags_df['date']<=date_h))

    # Construct category filter
    mask_category = tags_df['category']==category

    # Return filtered data
    return tags_df[mask_date & mask_category]


def get_graph(tags_df):
    
    # Eliminate filterning columns
    tags_df.drop(columns='date category method'.split(), inplace=True)

    # Drop NaNs
    tags_df.dropna(axis=0,inplace=True)

    # Delete duplicates
    tags_df = tags_df.drop_duplicates()

    # Only select summaries with +1 tag
    tags_by_summary = tags_df['geo_id mesh_id'.split()].groupby('geo_id').count().reset_index() # Count tags per summary
    good_summaries = tags_by_summary[tags_by_summary['mesh_id']>1] # Select abstracts with more than one tag
    clean_tags = pd.merge(tags_df, good_summaries, on='geo_id') # Inner Join
    clean_tags = clean_tags.drop(columns='mesh_id_y') # Drop column from inner join
    clean_tags = clean_tags.rename(columns={'mesh_id_x':'mesh_id'}) # Rename key column

    # Construct all-with-all links inside same geoid-nsample-date record
    links = pd.merge(tags_df, tags_df, on='geo_id nsamples'.split())
    
    # Rename to Source-Target
    links.rename(columns={'mesh_id_x':'source', 'mesh_id_y':'target'}, inplace=True)
    
    # Delete self-linkage
    links.drop(links[links['source']==links['target']].index, inplace=True)
    
    # Collapse repetitions while calculating weights
    links_weights = links.groupby('source target'.split()).sum().reset_index()
    
    # Rename sum(nsamples) to 'weight'
    links_weights.rename(columns={'nsamples':'weight'}, inplace=True)
    
    # Account for mirror-duplicates
    links_weights['weight']/=2
    
    # Normalize weights
    links_weights['weight']/=links_weights['weight'].max()
    
    # Save to .csv
    links_weights.to_csv(GEPHI_EDGES, index=False)
    
    # Construct Directed Graph
    az = nx.from_pandas_edgelist(links_weights, 
                                 source='source', 
                                 target='target', 
                                 edge_attr='weight', 
                                 create_using=nx.DiGraph()
                                 )

    # Return undirected graph
    return nx.to_undirected(az)


# Construct disease graph
disease_df = get_subselection(tags_df, '1990/01/01', '2019/01/01', 'C')
disease_g = get_graph(disease_df)
nx.write_gpickle(disease_g, DISEASE_GRAPH)


# Construct drug graph
drugs_df = get_subselection(tags_df, '1990/01/01', '2019/01/01', 'D')
drugs_g = get_graph(drugs_df)
nx.write_gpickle(drugs_g, DRUGS_GRAPH)






