# AstraZenecaMar19
For team AstraZeneca at March Virtual S2DS 2019

# Link to GoogleDrive documents
https://drive.google.com/drive/folders/1nHUJiPrvUruS4kLJrJSzfCdkm1UsYlwf

# Files uploaded:
        - AstraZeneca_project.docx   
        - BioPython snippets (Claire, Karsten, Luis)
        - test_NNN.csv (ID+Summary fro the first NNN-entries of the GEO DataBase)
        
        
# Information from project description

The goal of this project is to focus on the studies conducted on humans and use the text in the description to understand what disease areas are being studied, how this has changed over time, and what can be said about the future. 

Info on GEO website: https://www.ncbi.nlm.nih.gov/geo/info/overview.html

Main parts: 
1. Extract the text data from GEO 

a. Series homepage:
 https://www.ncbi.nlm.nih.gov/geo/browse/?view=series

b. Example experiment: 
https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE117746

c. Information on programmatic access: 
https://www.ncbi.nlm.nih.gov/geo/info/geo_paccess.html

2. Perform NLP analysis on the extracted text data

# DIRECTORY STRUCTURE
<hr>
<p>The directory structure of this project looks like this:</p>
<pre><code>├── LICENSE
├── Makefile           &lt;- Makefile with commands like `make data` or `make train`
├── README.md          &lt;- The top-level README for developers using this project.
├── data
│   ├── external       &lt;- Data from third party sources.
│   ├── interim        &lt;- Intermediate data that has been transformed.
│   ├── processed      &lt;- The final, canonical data sets for modeling.
│   └── raw            &lt;- The original, immutable data dump.
│
├── docs               &lt;- A default Sphinx project; see sphinx-doc.org for details
│
├── models             &lt;- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          &lt;- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── references         &lt;- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            &lt;- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        &lt;- Generated graphics and figures to be used in reporting
│
├── requirements.txt   &lt;- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze &gt; requirements.txt`
│
├── src                &lt;- Source code for use in this project.
│   ├── __init__.py    &lt;- Makes src a Python module
│   │
│   ├── data           &lt;- Scripts to download or generate data
│   │   └── make_dataset.py
│   │
│   ├── features       &lt;- Scripts to turn raw data into features for modeling
│   │   └── build_features.py
│   │
│   ├── models         &lt;- Scripts to train models and then use trained models to make
│   │   │                 predictions
│   │   ├── predict_model.py
│   │   └── train_model.py
│   │
│   └── visualization  &lt;- Scripts to create exploratory and results oriented visualizations
│       └── visualize.py
│
└── tox.ini            &lt;- tox file with settings for running tox; see tox.testrun.org
</code></pre>

