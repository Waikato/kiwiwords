#Loanword Co-occurrence Networks

This folder contains resources related to our paper on loanword networks:

- `network-analysis.py` contains most of the project code. The script builds a co-occurrence matrix by searching for loanwords in each of the 196 text files in the folder called `matariki-corpus`. It then creates several network files that can be loaded into [Gephi](https://gephi.org/). Files that help with drawing the aggregated hypergraphs are also generated.
- `all_n-grams.csv` contains a list of potential Māori words and phrases compiled from a large collection of New Zealand English (NZE) newspaper articles, including the Matariki Corpus, which is the corpus analysed in our paper.
- `loanwords.csv` contains a list of potential loanwords of interest.
- `coded_loans.csv` contains the manually-tagged properties for the chosen loanwords, including their borrowing type, semantic domain, size and listedness.
- `MAT-Clustering.r` contains code for running the hierarchical cluster analysis.

Five input files are also provided for loading the loanword sets into [PAOHVis](http://paovis.ddns.net/paoh.html): 
- These are the CSV files beginning with `paohvis_` (e.g. `paohvis_semantic_domain.csv`) 
- There is a separate CSV file for each categorical variable (borrowing type, semantic domain, size, listedness and frequency band)
- To load in the data, go to http://paovis.ddns.net/paoh.html
- By default, nodes will be arranged vertically by the number of sets they are part of (i.e. the node at the top belongs to the most sets). 
- Click on the button with the upwards arrow in the 'Data' tab, followed by 'Import Dataset'. Now load in the relevant data file.
- Go to the 'View' tab and change the number in the drips section to 1
- You can colour the data by the variable in the filename by clicking on the dropdown arrow next to 'community' (beneath the menu) and selecting 'community'
- You can group the data by the different caetgories by clicking on the dropdown arrow next to 'group by' (beneath the menu) and selecting 'community' 

Please email dtrye@waikato.ac.nz if you have any questions about these resources.