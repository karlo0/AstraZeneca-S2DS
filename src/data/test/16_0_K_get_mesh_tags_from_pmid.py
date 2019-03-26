# This script  fetches all gse series with Organism=Homo Sapiens of the GEO Database and creates a xml file out of it
from Bio import Entrez
Entrez.email = "karsten.leonhardt@posteo.de"
try:
    from urllib.error import HTTPError  # for Python 3
except ImportError:
    from urllib2 import HTTPError  # for Python 2
# retmax = maximum number of retrieved series

handle = Entrez.efetch(db="pubmed", id="10952317", retmode="xml")
record = Entrez.read(handle)
# - the MeSH tags are in the field elements of
# record['PubmedArticle'][0]['MedlineCitation']['MeshHeadingList']
# - ufortunately the list elements are strings so that they have to be broken up appropriately. The format is as follows:
#   'TAG', attributes={'UI': 'UI_NUMBER', 'MajorTopicYN': 'X'}
#   with:   TAG         - the MeSH tag as string
#           UI_NUMBER   - ID NUMBER of  

#for r in record:
#    print(r[')

a = record['PubmedArticle']
b = record['PubmedArticle'][0]['MedlineCitation']['MeshHeadingList']
#print(a[0])
#for k in range(len(a)):
#    print(a[k]['DescriptorName']+'\n')
