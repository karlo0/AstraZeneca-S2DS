March Virtual S2DS 2019 @ PIVIGO

# Team name
	nLp-AttaCK

# Team members
	Luis Vela 		vela.vela.luis@gmail.com
	Arun Narayanan 	arunisnowhere@gmail.com
	Claire Chambers 	chambers.claire@gmail.com
	Karsten Leonhardt 	karsten.leonhardt@posteo.de
	
# Link to shared Google Drive folder
	https://drive.google.com/drive/folders/1nHUJiPrvUruS4kLJrJSzfCdkm1UsYlwf

# Directory structure
	├── LICENSE
	├── README.md
	├── data (Google Drive)
	│	├── external       
	│   	├── interim        
	│   	├── final          
	│   	└── raw            
	├── docs               
	├── notebooks          
	├── reports            
	│   	└── figures        
	└── src                
    		├── data           
    		├── external       
    		├── features       
    		└── visualization 

# Naming convention 
	All the python notebooks and scripts comply with the following naming convention:
	
	WD_V_A_name.ext
	││ │ │ │    └── file extension
	││ │ │ └─────── file name
	││ │ └───────── author name (initial)
	││ └─────────── version
	│└───────────── day
	└────────────── week

# Company
	AstraZeneca (https://www.astrazeneca.com/)

# Company description
	AstraZeneca is a R&D pharmaceutical company with presence in research fields as varied as Cardiovascular, Respiratory, Autoimmune, Respiratory and Oncology. Their focus is mainly on disease and drug discovery.

# Company motivation
	Reduce the cost of drug discovery. Either by using existing drugs on different diseases or automatizing the process of running Differential Gene Analysis on existing, publicly available, gene expression databases.

# Company objective
	Automatize and scale the following processes:
	-Data Access
	-Data Exploration
	-Data Clustering and Labeling
	-Data visualization

# Project roadmap
	Three stages make up the process:
	-Programmatic access
	-Automated methods
	-Differential Expression Analysis

	How particular roadmap tackles the first two stages

# Concrete objectives   
	-Data analysis of the GEO database
		+Research trend analysis and forecast
		+Drug recommendation
	-Classification and labeling of genetic samples (Bonus)

# Raw resources
	We have access to the RAW information contained in the GEO database. The Gene-Expression-Omnibus (GEO) is a large public repository of genomic data submitted by the scientific community where users can query and download gene-expression studies and profiles for many species. In our case, we are concerned in the homo-sapiens case. See links below:
	https://www.ncbi.nlm.nih.gov/geo/info/overview.html
	https://www.ncbi.nlm.nih.gov/geo/browse/?view=series
	https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE117746
	https://www.ncbi.nlm.nih.gov/geo/info/geo_paccess.html 


# PART 1 - Querying GEO and generating data
# PART 2.1 - Drug Recommendation

	The drug recommendation is constructed via execution of the two following notebooks:
	
	- src/visualization/55_0_L_Disease_Drug_Graph.ipynb
	- src/visualization/55_0_L_Draw_Hierarchy.ipynb

	
## Subpart 2.1.1: 55_0_L_Disease_Drug_Graph.ipynb
	
### Imports
	-NumPy
	-Pandas
	-matplotlib 
	-NetworkX
 
### Input files
	'../../data/final/mesh.pkl'
	'../../data/final/geo.pkl'
	'../../data/final/geo_restful_chem.pkl'

### Step1. 
	Merge labels from geo.pkl and geo_restful_chem.pkl to take advantage of the more readable and more accurate tags for drug description that come from the restful API.

### Step2. 
	Calculate the category of each tag (Disease ‘C’ or Drug ‘D’. Calculate the depth in the hierarchical tree of each tagged disease/drug.

### Step3. 
	Filter entries by:
	-Date
	-Category
	-Depth
	And manually exclude subcategory C23 (Conditions, Signs and Symptoms)

### Step4. 
	Construct node-list for future graph creation. The list ought to contain node_id, node_label and node_category.

### Step5. 
	Construct edge_list for future graph creation. The list ought to contain:
	-Source (mesh_id)
	-Target (mesh_id)
	-Weight 

### Step6. 
	Construct the graph using the edge_list and load node attributes from node_list. Save as .pkl; Save as .gexf 

### Step7. 
	Select disease-only-subgraph. Run statistics:
	-EigenCentrality
	-PageRank
	-Degree

### Step8. 
	Measure all recommendation scores for top-n nodes (according to EigenCentrality metric). Rank them. 

### Step9. 
	Plot recommendation strength subgraph for a given cardinality using internal (limited) Network-X capabilities.

### Step10. 
	Repeat steps 7,8 and 9 for the drug-only subgraph to obtain a second-use recommendation for the most important drug-like nodes.


	
## Subpart 2.1.2: 55_0_L_Draw_Hierarchy.ipynb

### Imports:
	Matplotlib.pyplot
	Pandas
	Numpy
	NetworkX 
	Pygraphviz

### Input files
	../../data/interim/disease_parent_treenumbers.csv
	../../data/interim/disease_tree_heading_count.csv

### Step1. 
	Gather edge information. Resulting dataframe must contain two fields:
	-Source (Mesh_tree_id)
	-Target (Mesh_tree_id)

### Step2. 
	Gather node information. Resulting dataframe must contain three fields
	-Node_id (Mesh_tree_id)
	-Node_label (Mesh Heading)
	-Node_counts (Normalized number of counts)

### Step3. 
	Construct graph using edge_list and load node attributes from node_list. Save as .gexf.

### Step4. 
	Use NetworkX and Graphviz to construct a raw visualization of the hierarchical structure of the MeSH ontology. Use prog={‘sfdp’, ‘fdp’, ‘dot’, ‘twopi’ or ‘neato’}.


# PART 2.2 - Time Series Analysis
# PART 3 - Sample Classification (Bonus)
