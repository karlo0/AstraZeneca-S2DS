import pprint
import rdflib
from rdflib.plugins.sparql import prepareQuery

#init_mesh_bindings = {
#    'rdf': <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#    'rdfs': <http://www.w3.org/2000/01/rdf-schema#>
#    'xsd': <http://www.w3.org/2001/XMLSchema#>
#    'owl': <http://www.w3.org/2002/07/owl#>
#    'meshv': <http://id.nlm.nih.gov/mesh/vocab#>
#    'mesh': <http://id.nlm.nih.gov/mesh/>
#    'mesh2015': <http://id.nlm.nih.gov/mesh/2015/>
#    'mesh2016': <http://id.nlm.nih.gov/mesh/2016/>
#    'mesh2017': <http://id.nlm.nih.gov/mesh/2017/>
#    'mesh2018': <http://id.nlm.nih.gov/mesh/2018/>
#    'mesh2019': <http://id.nlm.nih.gov/mesh/2019/>
#}

#            'SELECT ?s WHERE { ?person foaf:knows ?s .}',
#            initNs = { "foaf": FOAF }

q = prepareQuery(
    """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>
    PREFIX mesh: <http://id.nlm.nih.gov/mesh/>
    PREFIX mesh2015: <http://id.nlm.nih.gov/mesh/2015/>
    PREFIX mesh2016: <http://id.nlm.nih.gov/mesh/2016/>
    PREFIX mesh2017: <http://id.nlm.nih.gov/mesh/2017/>

    SELECT ?treeNum ?ancestorTreeNum ?ancestor ?alabel
    WHERE { 
           mesh:D005138 meshv:treeNumber ?treeNum .
           ?treeNum meshv:parentTreeNumber+ ?ancestorTreeNum .
           ?ancestor meshv:treeNumber ?ancestorTreeNum .
           ?ancestor rdfs:label ?alabel .
    }"""
#    \
#    ORDER BY ?treeNum ?ancestorTreeNum'
#    initNs = init_mesh_bindings
)


g = rdflib.Graph()
#g.bind('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
#g.bind('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
#g.bind('xsd', 'http://www.w3.org/2001/XMLSchema#')
#g.bind('owl', 'http://www.w3.org/2002/07/owl#')
#g.bind('meshv', 'http://id.nlm.nih.gov/mesh/vocab#')
#g.bind('mesh', 'http://id.nlm.nih.gov/mesh/')
#g.bind('mesh2015', 'http://id.nlm.nih.gov/mesh/2015/')
#g.bind('mesh2016', 'http://id.nlm.nih.gov/mesh/2016/')
#g.bind('mesh2017', 'http://id.nlm.nih.gov/mesh/2017/')
#g.bind('mesh2018', 'http://id.nlm.nih.gov/mesh/2018/')
#g.bind('mesh2019', 'http://id.nlm.nih.gov/mesh/2019/')

g.load("../../data/raw/mesh.nt", format="nt")

print('dada')

for row in g.query(q):
    print(row)

#for stmt in g:
#        pprint.pprint(stmt)
#
#        # prints :
#            (rdflib.term.URIRef('http://bigasterisk.com/foaf.rdf#drewp'),
#              rdflib.term.URIRef('http://example.com/says'),
#              rdflib.term.Literal(u'Hello world'))
#            (rdflib.term.URIRef('http://bigasterisk.com/foaf.rdf#drewp'),
#              rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
#              rdflib.term.URIRef('http://xmlns.com/foaf/0.1/Person'))
