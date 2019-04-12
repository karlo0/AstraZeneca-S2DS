import pickle
import os

## Set paths
# cdir = dir of this script
cdir = os.path.dirname(os.path.realpath(__file__))
# basedir = root dir of the repository
basedir = os.path.dirname(os.path.dirname(cdir))

dir_data_in = basedir+"/data/interim/records_samples/samples_suppl/"
#dir_data_in = basedir+"/data/interim/records_samples/"

def import_df(fname):
    print("start load samples supp database")
    df = pickle.load( open(dir_data_in+fname, 'rb') )
    print("done")
    return df

# df = import_df('samples_suppl_0.pkl')
df = import_df('samples_suppl_15.pkl')
