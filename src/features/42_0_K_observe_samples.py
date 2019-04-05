import os
import pickle
## Set paths
# cdir = dir of this script
cdir = os.path.dirname(os.path.realpath(__file__))
# basedir = root dir of the repository
basedir = os.path.dirname(os.path.dirname(cdir))

dir_data_in = basedir+"/data/interim/records_samples/"

fname = "samples.pkl"

df = pickle.load( open(dir_data_in+fname, 'rb') )
