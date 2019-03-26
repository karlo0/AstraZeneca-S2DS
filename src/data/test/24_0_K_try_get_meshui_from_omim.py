# This script  fetches all gse series with Organism=Homo Sapiens of the GEO Database and creates a xml file out of it
from Bio import Entrez
Entrez.email = "karsten.leonhardt@posteo.de"
try:
    from urllib.error import HTTPError  # for Python 3
except ImportError:
    from urllib2 import HTTPError  # for Python 2
# retmax = maximum number of retrieved series

#handle = Entrez.einfo(db='medgen')
#record = Entrez.read(handle)
#
#print(record['DbInfo'].keys())
#omim  keys:
#['DbBuild', 'LinkList', 'MenuName', 'Description', 'FieldList', 'LastUpdate', 'DbName', 'Count']


#handle = Entrez.esearch(db="medgen", term="155600[MIM]")
#handle = Entrez.esearch(db="mesh", term="MELANOMA, CUTANEOUS MALIGNANT")
handle = Entrez.esearch(db="mesh", term="[C536395[MHUI]")
#
record0 = Entrez.read(handle)
handle.close()
#
#
#handle = Entrez.efetch(db="mesh", id=record0["IdList"][0], retmode="text", rettype="full")
#handle = Entrez.efetch(db="mesh", id=record0["IdList"][0], retmode="xml", rettype="xml")
handle = Entrez.esummary(db="mesh", id=record0["IdList"][0])
record = Entrez.read(handle)

handle2 = Entrez.esummary(db="mesh", id=str(int(record[0]['DS_HeadingMappedToList'][0])))
record2 = Entrez.read(handle2)

#
##record[0]['DS_IdxLinks'][1]['TreeNum']
