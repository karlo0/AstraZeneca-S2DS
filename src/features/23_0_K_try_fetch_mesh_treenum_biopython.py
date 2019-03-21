# This script  fetches all gse series with Organism=Homo Sapiens of the GEO Database and creates a xml file out of it
from Bio import Entrez
Entrez.email = "karsten.leonhardt@posteo.de"
try:
    from urllib.error import HTTPError  # for Python 3
except ImportError:
    from urllib2 import HTTPError  # for Python 2
# retmax = maximum number of retrieved series

handle = Entrez.esearch(db="mesh", term="D008545[MHUI] OR D005128[MHUI]")
#handle = Entrez.esearch(db="mesh", term="D005128[MHUI]")

record = Entrez.read(handle)
handle.close()


#handle = Entrez.efetch(db="mesh", id=record["IdList"][0], retmode="text", rettype="full")
#handle = Entrez.efetch(db="mesh", id=record["IdList"][0], retmode="xml", rettype="xml")
handle = Entrez.esummary(db="mesh", id=record["IdList"][0])
record = Entrez.read(handle)

#record[0]['DS_IdxLinks'][1]['TreeNum']
