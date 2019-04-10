"""Script to fetch detailed informations about all samples that are contained in the already fetched geo series"""
import numpy as np
import pandas as pd
import pickle
import os
import re
from itertools import compress
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import time
try:
    from urllib.error import HTTPError  # for Python 3
except ImportError:
    from urllib2 import HTTPError       # for Python 2

##<function section>##

# This function is for nested dictionaries of the structure as we generate below,
# and flattens list values where it makes sense and for list entries of length 1 
# it assigns the only list element as value to the key. In the special case where the key = 'channel_count'
# it tries to convert the str entry into an int
def list_flatten_in_dict(dct, key=None, match_list_in=None):
    if match_list_in == None:
        match_list = []
    else:
        match_list = match_list_in
    if isinstance(dct, dict):
        return {k: list_flatten_in_dict(v, key=k, match_list_in=match_list) for k, v in dct.items()}
    elif isinstance(dct, list):
        if len(dct) >= 1:
            if len(dct) == 1:
                if key == 'channel_count':
                    try:
                        return int(dct[0].strip())
                    except:
                        return dct[0].strip()
                else:
                    return dct[0].strip()
            elif (key != None) and (key in match_list):
                return " ".join(dct)
            else:
                return dct
        else:
            return None

##</function section>##


print("\n## fetch detailed informations about all samples that are contained in the already fetched geo series ##\n")


## Set paths
# cdir = dir of this script
cdir = os.path.dirname(os.path.realpath(__file__))
# basedir = root dir of the repository
basedir = os.path.dirname(os.path.dirname(cdir))


dir_data_in = basedir+"/data/interim/records_samples/"
dir_data_out = dir_data_in+"samples_suppl/"

# filenamebase for the large file containing all possibly relevant supplemental informations about the samples
fnameb_suppl = 'samples_suppl'
# filenamebase for the smaller file containing the informations about the channel characteristics of the samples only
fnameb_characteristics = 'samples_characteristics'

if not os.path.exists(dir_data_out):
    os.makedirs(dir_data_out)

def import_df(fname):
    print("start load samples database")
    df = pickle.load( open(dir_data_in+fname, 'rb') )
    print("done")
    return df

# import records dataframe
df_records = import_df('records.pkl')

# url base from which we query
urlbase = 'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?'

# pattern to read the lines of the fetched data:
# tries to catch the key and the corresponding value of each line, both as strings
pattern = re.compile(r"""^[!\^]Sample[\_]*(?P<key>\D*?)(_ch)*(?P<ch>\d*)\s*=\s*(?P<value>.*)$""", re.IGNORECASE)

# the list of channel specific keys of samples for which we want to extract the values
ch_key_list = ['source_name', 'characteristics', 'treatment_protocol', 'extract_protocol', 'growth_protocol', 'molecule']

# the list of general keys of samples for which we want to extract the value
gn_key_list = ['title', 'status', 'type', 'submission_date', 'channel_count', 'data_processing', 'description']

# keys for which we try to flatten their list entries by joining them as strings
keys_flt_vals = ['treatment_protocol', 'extract_protocol', 'growth_protocol', 'data_processing']

# dict for storing all possibly relevant informations of all samples
samples_supp = dict()

# dict for storing the channel characteristics of all samples only
samples_characteristics = dict()

# count the number of fetched samples, reset after each 10000 fetched samples
cnt_samples = 0

# global count the number of fetched samples, not reset
cnt_samples_glob = 0

# counter for files to be pickled
cnt_file = 0

# the number of samples whose informations are contained in each part of the to be written samples_supp dict
batchsize = 10000

# max number of samples to be fetched, if <= 0, fetch all available samples
max_samples = -1

flag_break = False

for acc_series in df_records['Accession']:
    print(acc_series)
    # urllib request string: acc_series is the geo series acc number
    #   tries to fetch all informations in the SOFT(form=text) format
    request = 'acc='+acc_series+'&targ=all&form=text&view=brief'

    code=404
    while(code == 404 or code == 501):
        try:
            urllib_query = urlopen(urlbase, request.encode())
        except HTTPError as e:
            code = e.code
            print("HTTPError: "+str(code))
            time.sleep(1)
        except URLError as e:
            code = e.code
            print("URLError: "+str(code))
            time.sleep(1)
        else:
            code = urllib_query.getcode()
    result_raw = urllib_query.read()
    result_raw = result_raw.decode('utf-8')
    result = result_raw.splitlines()
    ndxl = [i for i, x in enumerate(result) if x.startswith('^SAMPLE')]
    ndxl.append(len(result))
    for i in range(len(ndxl[0:-1])):
        sample_lines = result[ndxl[i]:ndxl[i+1]]
        match = pattern.match(sample_lines[0])
        sample_acc_id = match.group('value')
        if sample_acc_id not in samples_supp.keys():
            samples_supp[sample_acc_id] = dict()
            cnt_samples += 1
            cnt_samples_glob += 1
            print((cnt_samples_glob,sample_acc_id))
            sample_lines = sample_lines[1:]
            for line in sample_lines:
                match = pattern.match(line)
                if(bool(match)):
                    key = match.group('key')
                    ch  = match.group('ch')
                    val = match.group('value')
                    if len(ch) > 0:
                        ch = int(ch.strip())
                    else:
                        ch = 0
                    if key in gn_key_list:
                        if key not in samples_supp[sample_acc_id].keys():
                            samples_supp[sample_acc_id][key] = [val]
                        else:
                            samples_supp[sample_acc_id][key].append(val)
                    else:
                        if ch > 0:
                            if key in ch_key_list:
                                if ch not in samples_supp[sample_acc_id].keys():
                                    samples_supp[sample_acc_id][ch] = dict()
                                    samples_supp[sample_acc_id][ch][key] = [val]
                                else:
                                    if key not in samples_supp[sample_acc_id][ch].keys():
                                        samples_supp[sample_acc_id][ch][key] = [val]
                                    else:
                                        samples_supp[sample_acc_id][ch][key].append(val)

        samples_supp[sample_acc_id] = list_flatten_in_dict(samples_supp[sample_acc_id], match_list_in = keys_flt_vals)
        ch_count_list = list(set(list(samples_supp[sample_acc_id].keys())).difference(set(gn_key_list)))
        if len(ch_count_list) > 0:
            samples_characteristics[sample_acc_id] = dict()
            for k in ch_count_list:
                if 'characteristics' in samples_supp[sample_acc_id][k].keys():
                    samples_characteristics[sample_acc_id][k] = samples_supp[sample_acc_id][k]['characteristics']

        if cnt_samples == batchsize:
            # full filename for the part of the sample_supp dictionary to be stored to a file
            fname_suppl = fnameb_suppl+'_'+str(cnt_file)+'.pkl'
            # write to pickle file
            f = open(dir_data_out+fname_suppl,"wb")
            pickle.dump(samples_supp,f)
            f.close()
            # delete part of the sample_supp dictionary to restore space
            del samples_supp
            # set up new dict for samples_supp
            samples_supp = dict()
            # reset counter for samples
            cnt_samples = 0
            # increase counter that indicates the part of the samples_supp dict to be written to a file
            cnt_file += 1

        # break from inner loop when max_samples have been fetched
        if max_samples > 0:
            if cnt_samples_glob == max_samples:
                flag_break = True
                break

    # break from outer loop when max_samples have been fetched
    if flag_break:
        break

# write last part of the sample_supp dictionary to a file
fname_suppl = fnameb_suppl+'_'+str(cnt_file)+'.pkl'
# write to pickle file
f = open(dir_data_out+fname_suppl,"wb")
pickle.dump(samples_supp,f)
f.close()

# write the sample_characteristics dictionary to a file
fname_characteristics = fnameb_characteristics+'.pkl'
# write to pickle file
f = open(dir_data_out+fname_characteristics,"wb")
pickle.dump(samples_characteristics,f)
f.close()
