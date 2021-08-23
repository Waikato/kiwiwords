# -*- coding: utf-8 -*-

###########################################################################
#Code written by David Trye, University of Waikato, New Zealand

#Import modules
import os
import re
import pandas as pa
import numpy as np
import operator
from operator import itemgetter
import collections
from collections import Counter
import csv
#from operator import itemgetter
#NetworkX is a powerful network analysis library
import networkx as nx

###########################################################################

#Get current directory
DIR = os.path.dirname(os.path.realpath(__file__))

"""Runs the given method on all files in the directory with the specified file 
extension."""
def get_files(file_extension, method_to_call):
    for root, dirs, files in os.walk(DIR, topdown=False):   
        #For each file
        for filename in files:
            #If the current file's extension matches the one passed in
            if filename.endswith(file_extension):
                #Join filename with path to get location
                filePath = os.path.join(root, filename)            
                print("Processing %s..." % filename)
                method_to_call(filePath)

###########################################################################                
#GLOBAL VARIABLES
                
doc_cooccurrences = []
#Read in the manually-selected Māori n-grams from file
#NB: None of the loanwords in this file should be bracketed!
good_ngrams = pa.read_csv("loanwords.csv", sep=",")
good_ngrams = good_ngrams.sort_values(by=['n-gram'])
#Extract loans into a list
loanwords = good_ngrams['n-gram'].tolist()
#Add similar variants (will need to merge these later) 
loanwords.extend(['ki o rahi'])
#loanwords.extend(["kaupapa","kaupapa maori",
#                  "kohanga","kohanga reo",
#                  "kura kaupapa","kura kaupapa maori",
#                  "reo","te reo",
#                  "reo maori","te reo maori",
#                  "tikanga","tikanga maori"]) 
#Sort loans into alphabetical order
loanwords = sorted(loanwords)
print(loanwords)
print(len(loanwords))

#Get all candidate Māori n-grams from file    
#It is very important that 'non-maori' comes before 'maori' in the file
ngrams = pa.read_csv("all_ngrams.csv", sep=",")
#Sort n-grams from largest to smallest (important for ensuring 
#sub-n-grams are not counted in larger n-grams)
ngrams = ngrams.sort_values(by=['size'], ascending=False)
all_ngrams = ngrams['n-gram'].tolist()
#print(all_ngrams)  

props = ["semantic_domain","borrowing_type","size","listedness"]
colour_dict = {"core":"#28B36A","cultural":"#9A96E5","proper noun":"#F97743",
               "FF":"#28B36A","MC":"#00B7DA","PN":"#F97743","SC":"#9A96E5",
               "NO":"#3FB170","YES":"#EE7993",
               1:"#9A96E5",2:"#F97743",3:"#28B36A",6:"#00B7DA",7:"#FFFF00"}

filenames = []
trigger_loans = []

###########################################################################               
#GENERATE CO-OCCURRENCE MATRIX

"""Calculates the co-occurrence matrix for the loans of interest, 
and saves it to an output file"""
def compute_matrix(output_file):
    get_files(".txt", get_text_frequencies)
    #Check this works for 'non-maori'
    with open(output_file, 'w', encoding="utf8") as f:
        print("filename,year," + ",".join(loanwords),file=f)
        for doc in doc_cooccurrences:
            v = ",".join(map(str, doc))
            print(v, file=f)
    f.close()

"""Returns the plain text from the input file in a single string"""
def extract_text(input_file):
    reader = open(input_file, 'r', encoding='latin-1')
    text = reader.read()
    reader.close()
    return text

"""Calculates the number of occurrences of each loan in the given text"""
"""Need to call this function twice to deal with 'non-maori'"""
def get_text_frequencies(input_file):
    loanword_counts = {}
    text_cooccurrences = []
    #Extract corpus text as a string
    doc = extract_text(input_file)
    #Lower-case all letters
    doc = doc.lower()
    #Replace single quote marks and forward slashes with a blank space
    doc = doc.replace("'", " ")
    doc = doc.replace("/", " ")
    #For the MLW corpus only:
    #Fix instances of "maori" that have lost the "a" due to formatting issues
    doc = re.sub("\\bmori\\b", "maori", doc)
    #Replace numbers with a blank space
    doc = re.sub(r"(\d+)", r"\1 ", doc)
    #Replace newline characters with a space (in case an n-gram starts on 
    #one line and finishes on another)
    doc = doc.replace("\n", " ")
    #Merge multiple consecutive spaces into a single space
    doc = re.sub(" {2,}", " ", doc)
    #Insert spaces between punctuation
    doc = re.sub(r"([\w/'+$\s-]+|[^\w/'+$\s-]+)\s*", r"\1 ", doc)
    #Remove any macrons
    macrons = {'ā':'a','ē':'e','ī':'i','ō':'o','ū':'u'}
    for mac, plain in macrons.items():
        doc = doc.replace(mac, plain)
    #print(doc)
    #for each candidate Māori n-gram in the corpus
    for ngram in all_ngrams:
        #Also search for PLURAL lexicalised form (loan + 's', e.g. 'Kiwis')
        p = re.compile('\\b'+ngram+'\\b')
        p2 = re.compile('\\b'+ngram+'s\\b')
        #Used to just be:
        #p = re.compile('\\b'+ngram+'\\b')
        #For each loan of interest
        for lw in loanwords:
            #print(lw, ngram)
            #If current loan matches the current Māori n-gram 
            if lw == ngram:
                #Add the number of occurrences to the loanword counts dictionary
                loanword_counts[lw] = len(re.findall(p, doc))
                loanword_counts[lw] += len(re.findall(p2, doc))
        #Remove n-gram from corpus
        doc = re.sub(p, r"", doc)
    #print(loanword_counts)
    #Add filename to beginning of dictionary (this is hacky!)
    #Truncate path (remove everything before last back slash)
    input_file = re.sub(r".*\\", r"", input_file)
    #Matariki Corpus:
    year = re.sub(r".*(\d{4}).*", '\\1', input_file)    
    #Other Corpora:
    #year = re.sub(r".*_(\d{4})_.*", '\\1', input_file)
    loanword_counts['0' + input_file] = input_file
    loanword_counts[year] = year
    sorted_counts = sorted(loanword_counts, key=str.lower)
    for i in sorted_counts:
        text_cooccurrences.append(loanword_counts[i])
    doc_cooccurrences.append(text_cooccurrences)
    #print(text_cooccurrences)
    
"""Merges similar variants of loans, but only if both variants are present."""
def merge_similar_variants(input_file, output_file, corpus):
    #Read data from file
    matrix = pa.read_csv(input_file, sep=",")
    columns = list(matrix.columns)
    #Three 'parallel lists'
    if(corpus == "matariki"):
            version_a = ['kaupapa','kohanga','ki-o-rahi']
            version_b = ['kaupapa maori','kohanga reo','ki o rahi']
            merged = ['kaupapa (maori)','kohanga (reo)','ki(-)o(-)rahi']
    else:
        version_a = ['kaupapa','kohanga','kura kaupapa','reo','reo maori','tikanga', 'ki-o-rahi']
        version_b = ['kaupapa maori','kohanga reo','kura kaupapa maori','te reo',
                     'te reo maori','tikanga maori', 'ki o rahi']
        merged = ['kaupapa (maori)','kohanga (reo)','kura kaupapa (maori)',
                  '(te) reo','(te) reo maori','tikanga (maori)', 'ki(-)o(-)rahi']
    for i in range(0, len(version_a)):
        print("Merging", merged[i])
        if(version_a[i] in columns and version_b[i] in columns):
            matrix[merged[i]] = matrix[version_a[i]] + matrix[version_b[i]]   
            del matrix[version_a[i]]
            del matrix[version_b[i]]
#        elif(version_a[i] in columns and version_b[i] not in columns):
#            matrix.rename(columns={version_a[i]:merged[i]}, inplace=True)
#        elif(version_a[i] not in columns and version_b[i] in columns):
#            matrix.rename(columns={version_b[i]:merged[i]}, inplace=True)
    #Ensure consistent alphabetical ordering
    matrix.rename(columns={"ki(-)o(-)rahi":"ki-o-rahi"}, inplace=True)
    matrix = matrix.reindex(sorted(matrix.columns), axis=1)
    year = matrix.pop("year")
    filename = matrix.pop("filename")
    matrix.insert(0, year.name, year)  
    matrix.insert(0, filename.name, filename) 
    #Write to file
    matrix.to_csv(output_file, sep=",", header = True, index = False)    

def remove_infrequent_loans(input_file, output_file, THRESHOLD, dispersion, outliers):
    #Read data from file
    matrix = pa.read_csv(input_file, sep=",")
    #Remove first two columns (file metadata)
    year = matrix.pop("year")
    filename = matrix.pop("filename")
    columns = list(matrix.columns)
    print("Original number of loanwords:", len(columns))
    #Remove loanwords that do not feature in the corpus
    #https://stackoverflow.com/questions/21164910/how-do-i-delete-a-column-that-contains-only-zeros-in-pandas
    matrix = matrix.loc[:, (matrix != 0).any(axis=0)]
    #For each outlier passed in
    for outlier in outliers:
        #If the loan is present
        if outlier in columns:
            #Delete the corresponding column
            del matrix[outlier]       
        else:
            print("'{}' not in matrix".format(outlier))
    num_loans = len(list(matrix.columns))
    print("Loanwords with at least one occurrence:", num_loans)
    if(dispersion):               
        #https://stackoverflow.com/questions/33990495/delete-a-column-in-a-pandas-dataframe-if-its-sum-is-less-than-x
        matrix2 = matrix.drop([col for col, val in matrix.sum().iteritems() if val < THRESHOLD], axis=1, inplace=False)
        print("Loanwords that occur at least {} times: {}".format(THRESHOLD, len(list(matrix2.columns))))
        #Extract frequency dictionary
        freqs = matrix.sum().sort_values(ascending=False)
        freq_dict = freqs.to_dict()
        matrix[matrix > 1] = 1
        texts = matrix.sum().sort_values(ascending=False)
        text_dict = texts.to_dict()
        matrix.drop([col for col, val in matrix.sum().iteritems() if val < THRESHOLD], axis=1, inplace=True)    
        num_loans = len(list(matrix.columns))
        print("Loanwords that occur in at least {} texts: {}".format(THRESHOLD, num_loans))    
    else:
        matrix = matrix.drop([col for col, val in matrix.sum().iteritems() if val < THRESHOLD], axis=1, inplace=False)
        #Extract frequency dictionary
        freqs = matrix.sum().sort_values(ascending=False)
        freq_dict = freqs.to_dict()
        matrix[matrix > 1] = 1
        texts = matrix.sum().sort_values(ascending=False)
        text_dict = texts.to_dict()
        num_loans = len(list(matrix.columns))
        print("Loanwords that occur at least {} times: {}".format(THRESHOLD, num_loans))    
    
    #Get total number of loan types
    matrix['loan types'] = matrix.sum(axis=1)
    loan_types = matrix.pop("loan types")
    matrix.insert(0, loan_types.name, loan_types)         
    matrix['loan types graph'] = matrix['loan types']
    matrix.loc[(matrix['loan types graph'] >= 2),'loan types graph']='2+'
    matrix['loan types graph'] = matrix['loan types graph'].astype(str)
    loan_types_graph = matrix.pop("loan types graph")
    matrix.insert(0, loan_types_graph.name, loan_types_graph)         
    #Re-insert first two columns (file metadata)
    matrix.insert(0, year.name, year)  
    matrix.insert(0, filename.name, filename)
    #Write to file
    matrix.to_csv(output_file, sep=",", header = True, index = False)
    return freq_dict, text_dict
                       
###########################################################################               
#NETWORK ANALYSIS
#AUTOMATE THE SPREADSHEET STUFF THAT I USED TO DO MANUALLY!
#STILL NEED TO DO THE AGGREGATED ONES!

"""Generates the node file containing the coded linguistic properties 
and frequency of each loan. Calculates the logged normalised frequency of 
each loan."""
def generate_node_file(freq_dict, text_dict, tagged_data, output_file, corpus):
    tagged_loans = pa.read_csv(tagged_data, sep=",")
    if(corpus == "matariki"):
        TOTAL_WORDS = 91958
    elif(corpus == "mlw"):
        TOTAL_WORDS = 108521
    elif(corpus == "press"):
        TOTAL_WORDS = 5106998
    else:
        TOTAL_WORDS = 5307477
    with open(output_file, 'w', encoding="utf8") as f:
        print("node,logged_freq,size,semantic_domain,borrowing_type,listedness,frequency,nf*1000000,texts",file=f)
        for loan, freq in freq_dict.items():
            #Calculate normalised frequency per million words
            nf = freq / TOTAL_WORDS * 1000000
            texts = text_dict[loan]
            #Log the frequency for better range of node sizes in Gephi
            logged_freq = np.log10(nf)            
            size = tagged_loans.loc[tagged_loans["ngram"] == loan, "size"].to_string(index=False).strip()
            sem_dom = tagged_loans.loc[tagged_loans["ngram"] == loan, "semantic_domain"].to_string(index=False).strip()
            bor_type = tagged_loans.loc[tagged_loans["ngram"] == loan, "borrowing_type"].to_string(index=False).strip()
            listedness = tagged_loans.loc[tagged_loans["ngram"] == loan, "listedness"].to_string(index=False).strip()
            print("{},{},{},{},{},{},{},{},{}".format(loan, logged_freq, size, sem_dom, bor_type, listedness, freq, nf, texts),file=f)
    f.close()

"""Add columns with the colours for each coded property."""
def generate_node_colours(input_file, output_file):
    ngrams = pa.read_csv(input_file, sep=",")
    #https://stackoverflow.com/questions/20250771/remap-values-in-pandas-column-with-a-dict
    properties = ["semantic_domain","borrowing_type","size","listedness"]   
    #Only need to delete if present!
    if "frequency" in list(ngrams.columns):    
        del ngrams["frequency"]
    if "nf*1000000" in list(ngrams.columns):
        del ngrams["nf*1000000"]
    if "texts" in list(ngrams.columns):
        del ngrams["texts"]
    for prop in properties:
        ngrams['color_' + prop] = ngrams[prop]
        ngrams['color_' + prop] = ngrams['color_' + prop].map(colour_dict)
    ngrams.to_csv(output_file, sep=",", header = True, index = False)
    
def generate_aggregated_node_files(output_file):
    for prop in props:
        with open(output_file.replace(".csv", "_" + prop + ".csv"), 'w', encoding="utf8") as f:
            print("{},color".format(prop),file=f)
            if(prop == props[0]):
                keys = ["FF","PN","SC","MC"]
            elif(prop == props[1]):
                keys = ["core","cultural","proper noun"]
            elif(prop == props[2]):
                keys = [1,2,3,6,7]
            elif(prop == props[3]):
                keys = ["NO","YES"]
            for key in keys:
#                key2 = key
#                expanded = {1:"ONE",2:"TWO",3:"THREE",6:"SIX",7:"SEVEN"}
#                for num in expanded:
#                    if key == num:
#                        key2 = expanded[num]
#                print("{},{}".format(key2, colour_dict[key]),file=f)
                print("{},{}".format(key, colour_dict[key]),file=f)
        f.close()

"""Computes pairwise co-occurrences for loans in each text across the entire 
corpus. Also calculates the weight (frequency) of each pair."""
def get_edges(input_file, output_file, aggregate, unique, prop):
    rows = []
    #Get loanwords from co-occurrence matrix
    with open(input_file, 'r', encoding="utf8") as f:
        #The header with the loanwords
        header = f.readline().strip("\n").split(",")
        header = header[4:]
        for line in f:
            data = line.strip("\n").split(",")
            #Ignore filename, year and total columns
            data = data[4:]
            rows.append(data)
    #print(loanwords)
    #print(rows)
    index = -1
    cooccurrences = []
    all_cooccurrences = []
    #For each row
    for row in rows:
        #For each value in row
        for value in row:
            index += 1
            if(int(value) > 0):
                #Get loanword at index position
                #print(index)
                cooccurrences.append(header[index])
        index = -1
        #Sort loanwords alphabetically to ensure standard source->target order
        all_cooccurrences.append(sorted(cooccurrences))
        cooccurrences = []
    #print(all_cooccurrences)
    #print(all_cooccurrences[-4])
    all_edges2 = []    
    if(aggregate):
        edge = []
        #filename used to be "mlw-outliers-node-attributes.csv"
        ngrams = pa.read_csv("coded_loans.csv", sep=",")
        prop_values = ngrams[prop].tolist()
        nodes = ngrams['ngram'].tolist()
        for text in all_cooccurrences:
            #For each node in the current text
            for node in text:
                index = nodes.index(node)
                #print("Before:",node)
                node = prop_values[index]
                #print("After:",node)
                edge.append(node)
            #Sort properties alphabetically
            all_edges2.append(sorted(edge))
            edge = []
        #print(all_edges2[-4])    
    #Break down the entire set of loans into pairwise co-occurrences 
    all_edges = []
    if(aggregate):
        list_name = all_edges2
    else:
        list_name = all_cooccurrences
    for c in list_name:
        edges = [(c[i],c[j]) for i in range(len(c)) for j in range(i+1, len(c))]
        if(unique):
            #print("Edges:",edges)
            #print("Set edges:",set(edges))
            all_edges.append(set(edges)) #IS THIS THE RIGHT PLACE TO DO THIS?
        else:
            all_edges.append(edges)
        #print("")
        edges = []
        print(all_edges)   
    #Write loanword pairs to file
    with open(output_file, 'w', encoding="utf8") as f:
        for text in all_edges:
            #https://code-maven.com/python-iterate-list-of-tuples
            for field, value in text:
                print('{},{}'.format(field, value),file=f)
    f.close()   
    get_line_counts(output_file,output_file.replace(".csv","-weighted.csv"))
    
#Get line counts for output file produced by get_edges()
#https://stackoverflow.com/questions/14260406/python-how-to-count-how-many-lines-in-a-file-are-the-same
def get_line_counts(input_file, output_file):
    #In Bash, this is the same as:
    #Get line counts for output file (2-edges.csv)
    #sort 2-edges.csv | uniq -c > 2-edges-weighted.csv
    #Then open in sheets and download as CSV
    #Find: '(\d+) '
    #Replace with: '$1_' 
    with open(input_file) as f:
        counts = collections.Counter(l.strip() for l in f)
    f.close()
    with open(output_file, 'w', encoding="utf8") as writer:
        print("source,target,weight", file=writer)
        for line, count in counts.most_common():
            print("{},{}".format(line, count), file=writer)
    writer.close()

"""Calculates network statistics for the given nodes and edges, then generates
a .GEXF file for loading into Gephi. Based on the following tutorial:
https://programminghistorian.org/en/lessons/exploring-and-analyzing-network-data-with-python
"""
def process_network(node_file, edge_file, selection, output_file, stats_file, aggregated):    
    #Read the list of nodes from file
    with open(node_file, 'r') as nodecsv:
        nodereader = csv.reader(nodecsv)
        #Read all lines except the header, and put them all into the nodes list
        nodes = [n for n in nodereader][1:]
    #Extract only the node names (not the attribute data)
    node_names = [n[0] for n in nodes]
    #Read the list of edges from file
    with open(edge_file, 'r') as edgecsv: 
        edgereader = csv.reader(edgecsv)
        #Read all lines except the header, and put them into the edges list
        edges = [tuple(e) for e in edgereader][1:]
    #Create a new graph object, then add the list of nodes and edges
    G = nx.Graph() 
    G.add_nodes_from(node_names)    
    #Weighted edges uses a different property
    G.add_weighted_edges_from(edges)
    #Open file for saving summary statistics, including the type of graph,
    #number of nodes, edges and average degree
    with open(stats_file, 'w', encoding="utf8") as f:    
        print(nx.info(G), file=f)
        if(aggregated == False):    
            #Get node attibutes
            #Create a dictionary for each attribute
            logged_freq = {}
            size = {}
            semantic_domain = {}
            borrowing_type = {}
            listedness = {}
            color_semantic_domain = {}
            color_borrowing_type = {}
            color_size = {}
            color_listedness = {}        
            #Add attribute data to the appropriate node
            for node in nodes:
                logged_freq[node[0]] = float(node[1])
                size[node[0]] = node[2]
                semantic_domain[node[0]] = node[3]
                borrowing_type[node[0]] = node[4]
                listedness[node[0]] = node[5]                
                color_semantic_domain[node[0]] = str(node[6])
                color_borrowing_type[node[0]] = str(node[7])
                color_size[node[0]] = str(node[8])
                color_listedness[node[0]] = str(node[9])
            #Add node attributes to the graph object
            nx.set_node_attributes(G, logged_freq, 'logged_frequency')
            nx.set_node_attributes(G, size, 'size')
            nx.set_node_attributes(G, semantic_domain, 'semantic_domain')
            nx.set_node_attributes(G, borrowing_type, 'borrowing_type')
            nx.set_node_attributes(G, listedness, 'listedness')
            nx.set_node_attributes(G, color_semantic_domain, 'color_semantic_domain')
            nx.set_node_attributes(G, color_borrowing_type, 'color_borrowing_type')
            nx.set_node_attributes(G, color_size, 'color_size')
            nx.set_node_attributes(G, color_listedness, 'color_listedness')
        #If wanting to aggregate the data:
        else:
            color = {}
            for node in nodes:          
                color[node[0]] = str(node[1])
            nx.set_node_attributes(G, color, 'color')
        #Get the density (0 = no connection to 1 = every node is connected)
        density = nx.density(G)
        print("Network density:", density, file=f)
        #Calculate rgw shortest path between a given node and all others    
        #Get index of desired node   
        if(selection!=""):
            index = node_names.index(selection)
            with open("shortest-paths" + selection.replace(" ", "_") + ".csv", 'w', encoding="utf8") as fi:
                print("source,destination,length,path", file=fi)
                for node in node_names:
                    #Don't include node's path to itself
                    if(node != node_names[index]):
                        path = nx.shortest_path(G, source=node_names[index], target=node)
                        print("{},{},{},{}".format(node_names[index], node, len(path)-1, ",".join(path)), file=fi)
            fi.close()        
        #Returns false if graph has more than one component
        print(nx.is_connected(G),file=f)        
        #Get the list of connected components
        components = nx.connected_components(G)    
        #Find the largest component
        largest_component = max(components, key=len)
        #Create a "subgraph" of the largest component and calculate its diameter
        #Diameter is the longest of all shortest paths
        subgraph = G.subgraph(largest_component)
        diameter = nx.diameter(subgraph)
        print("Network diameter of largest component:", diameter,file=f)        
        triadic_closure = nx.transitivity(G)
        print("Triadic closure:", triadic_closure,file=f)            
        #Get the degree (i.e. number of connections a node has to other nodes)
        #Only conisders immediate neighbours
        degree_dict = dict(G.degree(G.nodes()))       
        #Find the top 20 nodes, ranked by degree
        sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)
        print("Top 20 nodes by degree:")
        for d in sorted_degree[:20]:
            print(d)           
        #Betweenness centrality - what proportion of shortest paths go through 
        #the given node?
        betweenness_dict = nx.betweenness_centrality(G)
        #Get top 20 nodes by betweenness centrality
        sorted_betweenness = sorted(betweenness_dict.items(), key=itemgetter(1), reverse=True)
        print("Top 20 nodes by betweenness centrality:")
        for b in sorted_betweenness[:20]:
            print(b)  
        #Eigenvector centrality    
        eigenvector_dict = nx.eigenvector_centrality(G)
        #Get top 20 nodes by eigenvector
        sorted_eigenvectors = sorted(eigenvector_dict.items(), key=itemgetter(1), reverse=True)
        print("Top 20 nodes by eigenvector:")
        for b in sorted_eigenvectors[:20]:
            print(b)       
        #Save all metrics as node attributes (except for modularity - only works for non-weighted links)
        nx.set_node_attributes(G, degree_dict, 'degree')
        nx.set_node_attributes(G, betweenness_dict, 'betweenness')
        nx.set_node_attributes(G, eigenvector_dict, 'eigenvector')   
        print("", file=f)
        print("n-gram,betweenness_centrality,degree,eigenvector", file=f)
        #Display both betweenees and degree of all nodes
        for tb in sorted_betweenness:
            #Use degree_dict to access a node's degree, see footnote 2
            degree = degree_dict[tb[0]] 
            eigenvector = eigenvector_dict[tb[0]]
            print("{},{},{},{}".format(tb[0], tb[1], degree, eigenvector), file=f)
    f.close()
    #Save the graph object to a GEXF file, for use in Gephi
    nx.write_gexf(G, output_file)

###########################################################################               
#TRIGGER LOAN ANALYSIS
    
"""Extracts the 'trigger loan' in each text file: 
    the first loan (from the list of nodes) to occur in the file."""
def get_all_triggers(output_file):
    get_files(".txt", get_trigger_loan)    
    with open(output_file, 'w', encoding="utf8") as f:
        print("filename,trigger",file=f)
        count = 0
        for file in filenames:
            #This may include files with only one loanword!
            #if(trigger_loans[count] != "N/A"):
            print("{},{}".format(file, trigger_loans[count]), file=f)
            count+=1 
    f.close()
    
"""Appends the trigger loan to the co-occurrence matrix"""
#https://stackoverflow.com/questions/25493625/vlookup-in-pandas-using-join
def add_triggers(input_file1, input_file2, output_file):
    #Read in trigger loans
    triggers = pa.read_csv(input_file1, sep=",")
    #Read in cooccurrence matrix
    matrix = pa.read_csv(input_file2, sep=",")
    matrix = matrix.merge(triggers, on='filename', how='left')
    matrix.to_csv(output_file, sep=",", index=False)    

"""Calculates the fist loan to occur in the given text
SHOULD USE A LIST WITH ALL LOANS THAT APPEAR IN THE CO-OCCURRENCE MATRIX
BUT DON'T WANT BRACKETED VARIANTS - AS THEY ARE NOT WRITTEN LIKE THAT IN TEXT
Also need to update the conditional statements for the bracketed variants 
according to which corpus is being used!
"""
def get_trigger_loan(input_file):
    indices = []
    doc = extract_text(input_file)
    doc = doc.lower()
    doc = doc.replace("'", " ")
    doc = doc.replace("/", " ")
    #For the MLW corpus only:
    doc = re.sub("\\bmori\\b", "maori", doc)
    doc = re.sub(r"(\d+)", r"\1 ", doc)
    doc = doc.replace("\n", " ")
    doc = re.sub(" {2,}", " ", doc)
    #Insert spaces between punctuation
    doc = re.sub(r"([\w/'+$\s-]+|[^\w/'+$\s-]+)\s*", r"\1 ", doc)
    #Remove macrons
    macrons = {'ā':'a','ē':'e','ī':'i','ō':'o','ū':'u'}    
    for mac, plain in macrons.items():
        doc = doc.replace(mac, plain)
    #print(doc)
    loanwords_present = []
    #Get list of all loanwords that occur in the text
    for loanword in loanwords:
        #if loanword = "(te) reo"
            #loanword = "te reo"
        p = re.compile(" " + loanword + " ")    
        result = p.search(doc)    
        if(result != None):
            loanwords_present.append(loanword)
    #print(loanwords_present) 
    #for each loan present in the text
    for loanword in loanwords_present:
        #Calculate index of its first occurrence (or return -1 if it doesn't occur)
        tmp = get_first_index(loanword, doc)
        #If it occurs in the text
        if(tmp[0] != -1):
            indices.append(tmp)
    #Return longest n-gram at min index
    #Sort list of tuples by indices
    indices.sort(key = operator.itemgetter(0))
    print(indices)
    #Get index of first ('trigger' loanword
    if(len(indices)>0):
        min_value = indices[0][0]
        #Find all n-grams with that index
        candidate_loans = [item for item in indices if min_value in item]
        #Then get the longest n-gram
        #https://stackoverflow.com/questions/13145368/find-the-maximum-value-in-a-list-of-tuples-in-python
        #Trigger loans and filenames are parallel lists 
        #Given index corresponds to same file
        #HANDLE MERGED VARIANTS
        trigger = max(candidate_loans,key=itemgetter(1))[1]
        if trigger == "kaupapa" or trigger == "kaupapa maori":
            trigger = "kaupapa (maori)"
        elif trigger == "kohanga" or trigger == "kohanga reo":
            trigger = "kohanga (reo)"
#        elif trigger == "kura kaupapa" or trigger == "kura kaupapa maori":
#            trigger = "kura kaupapa (maori)"        
#        elif trigger == "reo" or trigger == "te reo":
#            trigger = "(te) reo"     
#        elif trigger == "reo maori" or trigger == "te reo maori":
#            trigger = "(te) reo maori"
#        elif trigger == "tikanga" or trigger == "tikanga maori":
#            trigger = "tikanga (maori)"
        print(trigger)
        trigger_loans.append(trigger)
    else:
        trigger_loans.append("N/A")
    input_file = re.sub(r".*\\", r"", input_file)
    filenames.append(input_file)
    #print(trigger_loans)

"""Determines the position of the first occurrence of each loan in the text"""
def get_first_index(loanword, doc):
    #https://stackoverflow.com/questions/14919171/how-can-i-find-a-first-occurrence-of-a-string-from-a-list-in-another-string-in-p    
    #Don't count substrings ("iwi" shouldn't return a match for "kiwi")    
    #print(loanword)
    super_loans = []
    #Remove any larger n-grams containing the loanword
    for ngram in all_ngrams:
        p = re.compile("\\b" + loanword + "\\b") 
        result = p.search(ngram)
        if(result != None and loanword != ngram):
            super_loans.append(ngram)
    #print(super_loans)
    #print(doc)
    doc2 = doc
    for loan in super_loans:    
        #Remove n-gram from doc
        #Don't modify the original doc, make a copy called doc2
        p = re.compile(" " + loan + " ")    
        doc2 = re.sub(p, r"", doc2)
    #print(doc2)
    #print(loanword)
    p = re.compile(" " + loanword + " ")    
    result = p.search(doc2) #used to be doc 
    #print(result)
    if(result != None):
        search = result.group(0)
    else:
        search = "ZZrandomZZ"
    try:
        return doc2.index(search), loanword
    except ValueError:
        return -1, "N/A"         

###########################################################################
#HYPERGRAPH ANALYSIS

"""Extracts the complete set of loans in each text and saves them to file."""
def get_paoh_edges(input_file, generate_paoh, aggregate_timeslots):
    rows = []
    years = []
    #Get loanwords from co-occurrence matrix
    with open(input_file, 'r', encoding="utf8") as f:
        #The header with the loanwords
        header = f.readline().strip("\n").split(",")
        #Remove first four items (filename, year and totals) from header (so it just contains loanwords)
        header = header[4:]
        for line in f:
            data = line.strip("\n").split(",")
            years.append(data[1])
            data = data[4:]
            rows.append(data)
    #print(loanwords)
    #print(rows)
    index = -1
    cooccurrences = []
    all_cooccurrences = []
    #edges = []
    all_edge_ids = []
    #For each row
    for row in rows:
        #For each value in row
        for value in row:
            index += 1
            if(int(value) > 0):
                #Get loanword at index position
                #print(index)
                cooccurrences.append(header[index])
        index = -1
        #Loanwords sorted alphabetically to ensure standard source->target order
        all_cooccurrences.append(sorted(cooccurrences))
        #Remove spaces from phrases
        #edges = [c.replace(' ', '') for c in cooccurrences]
        all_edge_ids.append("_".join(cooccurrences)) #edges
        cooccurrences = []    
    #print(all_cooccurrences)
    #print(years)
    #print(all_edge_ids)
    
    #Generate standard PAOHVis input file
    #NB: Doesn't remove duplicate relationships, but PAOVHis ignores these
    if(generate_paoh):
        count = 0
        with open("paohvis.csv", 'w', encoding="utf8") as f:
            for cooccurrence in all_cooccurrences:
                #If there are at least two loanwords in the document
                if(len(cooccurrence)>1):
                    for ngram in cooccurrence:
                        print('{},{},{}'.format(all_edge_ids[count], ngram, years[count]), file=f)
                count += 1
        f.close()
    
    count = 0
    if(aggregate_timeslots):
        output_file = "relationships_aggregated.csv"
        header = "hyperedge,k"
    else:
        output_file = "relationships_years.csv"
        header = "hyperedge,k,year"
    with open(output_file, 'w', encoding="utf8") as f:
        print(header, file=f)
        for cooccurrence in all_cooccurrences:
            #If there are at least two loanwords in the document
            if(len(cooccurrence)>1):
                #Get the size of the relationship (the value of k)
                size = all_edge_ids[count].count('_') + 1
                if(aggregate_timeslots):
                    #Don't append year
                    print('{},{}'.format(all_edge_ids[count], size), file=f)
                else:
                    print('{},{},{}'.format(all_edge_ids[count], size, years[count]), file=f)
            count += 1
    f.close()
    split_paoh_by_k(output_file, aggregate_timeslots)

"""Partitions the PAOHVis sets by set: one size per file."""
#PAOH FORMAT (ONE ROW FOR EACH NODE IN THE RELATIONSHIP)
def split_paoh_by_k(input_file, aggregate_timeslots):
    relationships = pa.read_csv(input_file, sep=",")
    grouped = relationships.groupby('k')
    #For all hyperedges with same k
    for name, group in grouped:
        count=0
        #Put edge ids into list
        edge_ids = group['hyperedge'].tolist()
        output_file_prefix = "paohvis-aggregated-k" 
        if(aggregate_timeslots == False):
            #Put years into list
            output_file_prefix = "paohvis-years-k"
            years = group['year'].tolist()
        #For each n-gram (node) in the relationship 
        with open(output_file_prefix + str(name) + ".csv", 'w', encoding="utf8") as f:
            for edge_id in edge_ids:
                #Split edge id into individual n-grams
                edge_id = edge_id.split("_")
                #print(edge)
                #For each n-gram in the edge id
                for ngram in edge_id:
                    #Write the edge id, ngram and count to file
                    if(aggregate_timeslots):
                        print('{},{},{}'.format(edge_ids[count], ngram, "all_years"), file=f)
                    else:    
                        print('{},{},{}'.format(edge_ids[count], ngram, years[count]), file=f)
                #Increment count
                count+=1
            #Reset count
            count=0
    
#PAOH FORMAT (ONE ROW FOR EACH NODE IN THE RELATIONSHIP)
"""Alternative method for generating the PAOHVis file - uses a spreadsheet
with the weight/frequency of each set."""
def encode_paoh_weights(input_file):
    relationships = pa.read_csv(input_file, sep=",")
    #recurring-sets-weighted-adjusted3
    with open("paohvis-adjusted.csv", 'w', encoding="utf8") as f:  
        #count = 1            
        for i, row in relationships.iterrows():
            print(row.name, row['hyperedge'])
            #Split edge id into individual n-grams
            hyperedge = row['hyperedge']
            hyperedge = hyperedge.split("_")
            weight = row['weight']
            #for i in range(count,count+weight+1):
            for i in range(1,weight+1):
                #print(count)
                for ngram in hyperedge:
                    print('{},{},{}'.format(row['hyperedge'],ngram,i),file=f)
                #count +=1
                #print('{},{},{}'.format(row['hyperedge'],hyperedge[0],i),file=f)
                   
#Get line counts for output file produced by get_edges()
#https://stackoverflow.com/questions/14260406/python-how-to-count-how-many-lines-in-a-file-are-the-same
def get_hyperedge_counts(input_file, output_file):
    with open(input_file) as f:
        counts = collections.Counter(l.strip() for l in f)
    f.close()
    with open(output_file, 'w', encoding="utf8") as writer:
        print("hyperedge,k,weight,year", file=writer)
        for line, count in counts.most_common():
            if "hyperedge" not in line:
                print("{},{}".format(line, count), file=writer)
    writer.close()

###########################################################################
#CUSTOM AGGREGATED HYPERGRAPHS

#Code largely copied from get_edges() function - could be more efficient!
def generate_aggregated_hypergraph(input_file, aggregate, unique, prop):
    rows = []
    #Get loanwords from co-occurrence matrix
    with open(input_file, 'r', encoding="utf8") as f:
        #The header with the loanwords
        header = f.readline().strip("\n").split(",")
        header = header[4:]
        for line in f:
            data = line.strip("\n").split(",")
            #Ignore filename, year and totals
            data = data[4:]
            rows.append(data)
    #print(loanwords)
    #print(rows)
    index = -1
    cooccurrences = []
    all_cooccurrences = []
    #For each row
    for row in rows:
        #For each value in row
        for value in row:
            index += 1
            if(int(value) > 0):
                #Get loanword at index position
                #print(index)
                cooccurrences.append(header[index])
        index = -1
        #Sort loanwords alphabetically to ensure standard source->target order

        #Filter out texts containing only one loan
        num_loans = len(sorted(cooccurrences))
        if num_loans > 1:
            all_cooccurrences.append(sorted(cooccurrences))
        cooccurrences = []
    #print(all_cooccurrences)
    #print(all_cooccurrences[0])
    
    #agg_set
    all_edges2 = []    
    if(aggregate):
        edge = []
        #filename used to be "mlw-outliers-node-attributes.csv"
        ngrams = pa.read_csv("nodes.csv", sep=",")
        prop_values = ngrams[prop].tolist()
        nodes = ngrams['node'].tolist()
        #size = ngrams['size'].tolist()
        for text in all_cooccurrences:
            #Get index of c in nodes list
            for node in text:
                index = nodes.index(node)
                #print("Before:",node)
                node = prop_values[index]
                #print("After:",node)
                edge.append(node)
            #Sort properties alphabetically
            all_edges2.append(sorted(edge))
            edge = []
        #print(all_edges2)
        
        #THIS DOES VERSION A
        all_distinct_categories = []
        #Get distinct categories
        for loan_set in all_edges2:
            all_distinct_categories.append(list(set(loan_set)))
        #Merge distinct categories - get a count of each
        #https://stackoverflow.com/questions/45019607/count-occurrence-of-a-list-in-a-list-of-lists
        #print(all_distinct_categories)
        all_distinct_categories_merged = map(tuple, all_distinct_categories)
        count = Counter(all_distinct_categories_merged)
        #print(count.most_common())        
        with open("result_" + prop + ".csv", 'w', encoding="utf8") as writer:
            for key, value in count.most_common():
                print(str(value) + "\t", end="",file=writer)
                for cat in key:
                    print(str(cat) + "\t", end="",file=writer)
                print("",file=writer)
        writer.close()
        
        
#        for key, value in count.most_common():
#            print(str(value) + "\t", end="")
#            for i in range(0,len(all_distinct_categories)):                
#                if key[i] == all_distinct_categories[i]:
#                    print(key[i] + "\t", end="") 
#                else:
#                    print("\t", end="")                
#                print("")

        
        #VERSION B
        all_configs = []
        all_configs2 = []
        maximum = {}
        for loan_set in all_edges2:
            #Count how many times each value occurs 
            config = []
            config2 = {}
            for loan in sorted(set(loan_set)):
                new_loan = loan
                if(loan == 1):
                    new_loan = "one"
                elif(loan == 2):
                    new_loan = "two"
                elif(loan == 3):
                    new_loan = "three"
                elif(loan == 4):
                    new_loan = "four"
                elif(loan == 6):
                    new_loan = "six"
                elif(loan == 7):
                    new_loan = "seven"
                #print(loan, loan_set.count(loan))
                config.append((str(new_loan) + "\t") * loan_set.count(loan))
                config2[new_loan] = loan_set.count(loan)
                #print(maximum)               
                if(new_loan not in maximum):
                    maximum[new_loan] = loan_set.count(loan)
                else:
                    if(loan_set.count(loan) > maximum[new_loan]):
                        maximum[new_loan] = loan_set.count(loan)
                
                #print(str(new_loan), loan_set.count(loan), end="\t")
            #print("")
            joined_configs = "".join(config)
            #print(joined_configs)
            #print("")
            all_configs.append(joined_configs)
            all_configs2.append(config2)
        #print(all_configs2)
       # print(all_configs)     
        with open("result2_" + prop + ".csv", 'w', encoding="utf8") as writer:
            for config in set(all_configs):
                count = all_configs.count(config)
                print(str(count) + "\t", config, file=writer)
        f.close()
        return maximum
        

def update_file(input_file, dict1, prop):
     print(dict1)
     with open(input_file, 'r', encoding="utf8") as f:
        with open("result3_" + prop + ".csv", 'w', encoding="utf8") as writer:
            for line in f:
                freq = line.split("\t")
                print(freq[0], end = "\t", file=writer)
                for key, value in dict1.items():
                    count = line.count(key)
                    #print("Key:", key)
                    #print("Count:", count)
                    #Tabs to add
                    tabs_to_add = value - count
                    #print("Tabs to add", tabs_to_add)
                    print(((key + "\t") * count), end = "", file=writer)
                    print(("\t" * tabs_to_add), end = "", file=writer)
                print("",file=writer)
                        #print("\t" * tabs_to_add, end = "")

#       for config in set(all_configs):
#            count = all_configs.count(config)
#            print(count, end="\t")
#            new_config = config.split(",")
#            #for c in new_config:
#                #print(c)
#            print("")
    
###########################################################################
#METRICS
                        
#NB: Could have operated on the original doc array directly instead of the list of relationships
def compute_metric(inputFile1, inputFile2, inputFile3):
    #Read in good (manually-selected) n-grams from file
    good_ngrams = pa.read_csv("nodes.csv", sep=",")
    good_ngrams = good_ngrams.sort_values(by=['node'])
    good_ngrams['node'] = good_ngrams['node'].apply(lambda x: re.sub("\(","", x))
    good_ngrams['node'] = good_ngrams['node'].apply(lambda x: re.sub("\)","", x))
    loanwords = good_ngrams['node'].tolist()    
    #print("")
    #print(loanwords)
    #Weighted edges
    aggregated_edges = pa.read_csv(inputFile1, sep=",")
    year_edges = pa.read_csv(inputFile2, sep=",")
    triggers = pa.read_csv(inputFile3, sep=",")
    with open("2-metrics.csv", 'w', encoding="utf8") as f:                
        print("n-gram,total_sets,distinct_sets,mean_set_freq,degree,avg_length,max_weight",file=f)
        for lw in loanwords:
            #Use regex to search for n-gram listed at beginning, middle or end of relationship:
            #^matariki_|_matariki_|_matariki$    
            relationships = aggregated_edges[aggregated_edges['hyperedge'].str.contains('^' + lw + '_|_' + lw + '_|_' + lw + "$", regex=True, na=False)]
            breadth_dict = {}
            for relationship in relationships['hyperedge']:
                #if "(" in relationship:
                #    print(relationship)
                #relationship = relationship.replace("(", "")
                #relationship = relationship.replace(")", "")
                nodes = relationship.split("_")
                for node in nodes:
                    if node in breadth_dict:
                        breadth_dict[node] += 1
                    else:
                        breadth_dict[node] = 1
            #print(breadth_dict)
            breadth = len(breadth_dict)-1
            if(breadth<0):
                breadth = 0
            #print(lw, breadth)
            cumulative_weight = relationships['weight'].sum()
            max_weight = relationships['weight'].max()
            depth = len(relationships)
            mean_weight = round(relationships['weight'].mean(), 2)
            #In addition to average length, could calculate min and max
            avg_length = round((relationships['hyperedge'].str.count('_').sum()+len(relationships))/len(relationships),2)
            print("{},{},{},{},{},{},{}".format(lw, cumulative_weight, depth, mean_weight, breadth, avg_length, max_weight), file=f)
    f.close()
    #Calculate a node's persistence across time
    #Could potentially calculate stats so that same relationship in different years is treated differently - but likely to suffer from data sparsity!      
    with open("2-metrics2.csv", 'w', encoding="utf8") as f:
        print("n-gram,persistence",file=f)
        for lw in loanwords:
            #Create a subset of the dataframe with relationships containing the given loanword
            relationships = year_edges[year_edges['hyperedge'].str.contains('^' + lw + '_|_' + lw + '_|_' + lw + "$", regex=True, na=False)]
            #Count how many different years there are
            persistence = relationships['year'].nunique()
            print("{},{}".format(lw, persistence), file=f)
    f.close()
    #Trigger occurrences - be sure to only count texts with RELATIONSHIPS (i.e. two or more loanwords)
    with open("2-metrics3.csv", 'w', encoding="utf8") as f:
        print("n-gram,trigger_occurrences",file=f)
        for lw in loanwords:
            nodes = triggers[triggers['trigger'] == lw]
            trigger_occurrences = nodes['trigger'].count()
            print("{},{}".format(lw, trigger_occurrences), file=f)
    f.close()
    #Distinct nodes - breadth of relationship
    #Use regex to determine whether a lw is present in a relationship
    #Could derive a list of occurrences, then tally up distinct nodes??
    
#https://stackoverflow.com/questions/25493625/vlookup-in-pandas-using-join
def merge_files(inputFile1, inputFile2, inputFile3, outputFile):
    all_metrics = pa.read_csv(inputFile1, sep=",")
    persistence = pa.read_csv(inputFile2, sep=",")
    trigger_occurrences = pa.read_csv(inputFile3, sep=",")
    
    all_metrics = all_metrics.merge(persistence, on='n-gram', how='left')
    all_metrics = all_metrics.merge(trigger_occurrences, on='n-gram', how='left')
    all_metrics['trigger_ratio'] = round(all_metrics['trigger_occurrences'] / all_metrics['total_sets'], 2)   
    all_metrics.to_csv(outputFile, sep=",", index=False) 
            
        
############################################################################
##########################   FUNCTION CALLS   ##############################                 
############################################################################

#MATARIKI CORPUS: STANDARD NETWORKS
        
#Generate co-occurrence matrix
#Remember to change rege for other corpora, so that the year is correctly
#extracted from the filename
compute_matrix("matariki.csv")
#Merge similar variants into a single bracketed form
merge_similar_variants("matariki.csv", "matariki-merged.csv","matariki")

#Loans that occur at least five times
freq_dict, text_dict = remove_infrequent_loans("matariki-merged.csv", 
                                               "matariki-matrix.csv", 
                                               5, False, ["matariki"])
#Arguments: input_file, output_file, aggregate, unique, prop
get_edges("matariki-matrix.csv","edges.csv",False,False,"N/A")
generate_node_file(freq_dict, text_dict, "coded_loans.csv", 
                   "nodes.csv", "matariki")
generate_node_colours("nodes.csv", "nodes-colors.csv")
process_network("nodes-colors.csv", "edges-weighted.csv", "", "output.gexf", 
                "output-stats.csv",False)

#Loans that occur at least five times, with Māori removed
freq_dict, text_dict = remove_infrequent_loans("matariki-merged.csv", 
                                               "matariki-outlier-removed-matrix.csv", 
                                               5, False, ["matariki","maori"])
get_edges("matariki-outlier-removed-matrix.csv","edges-outlier-removed.csv",False,False,"N/A")
generate_node_file(freq_dict, text_dict, "coded_loans.csv", 
                   "nodes-outlier-removed.csv", "matariki")
generate_node_colours("nodes-outlier-removed.csv", "nodes-outlier-removed-colors.csv")
process_network("nodes-outlier-removed-colors.csv", 
                "edges-outlier-removed-weighted.csv", "", 
                "output-outlier-removed.gexf", 
                "output-outlier-removed-stats.csv",False)

#Generate aggregated networks
generate_aggregated_node_files("nodes_agg.csv")
for prop in props:
    #At least five texts
    get_edges("matariki-matrix.csv","edges_agg_" + prop + ".csv",True,False,prop)        
    get_edges("matariki-matrix.csv","edges_agg_" + prop + "_unique.csv",True,True,prop)
    process_network("nodes_agg_" + prop + ".csv", "edges_agg_" + prop + "-weighted.csv", "", "output_agg_" + prop + ".gexf", "output_agg_" + prop + "_stats.csv",True)
    process_network("nodes_agg_" + prop + ".csv", "edges_agg_" + prop + "_unique-weighted.csv", "", "output_agg_" + prop + "_unique.gexf", "output_agg_" + prop + "_stats.csv",True)
    #Maori removed
    get_edges("matariki-outlier-removed-matrix.csv","edges_outlier_removed_agg_" + prop + ".csv",True,False,prop)        
    get_edges("matariki-outlier-removed-matrix.csv","edges_outlier_removed_agg_" + prop + "_unique.csv",True,True,prop)
    process_network("nodes_agg_" + prop + ".csv", "edges_outlier_removed_agg_" + prop + "-weighted.csv", "", "output_outlier_removed_agg_" + prop + ".gexf", "output_outlier_removed_agg_" + prop + "_stats.csv",True)
    process_network("nodes_agg_" + prop + ".csv", "edges_outlier_removed_agg_" + prop + "_unique-weighted.csv", "", "output_outlier_removed_agg_" + prop + "_unique.gexf", "output_outlier_removed_agg_" + prop + "_unique_stats.csv",True)
#Need to delete any categories which are not present (e.g. 5 & 6 for loan size)   

###########################################################################

#TRIGGER LOAN ANALYSIS
get_all_triggers("matariki-triggers.csv")
add_triggers("matariki-triggers.csv", "matariki-matrix.csv", "matariki-matrix2.csv")

###########################################################################
#HYPERGRAPH ANALYSIS
#First boolean is whether to generate standard PAOH file (including timeslots)
#Second boolean is whether to the aggregated sets of relationships (=True) or 
#the year-by-year sets (=False)  

#get_paoh_edges with YEAR data
get_paoh_edges("matariki-matrix.csv", True, True)
get_paoh_edges("matariki-matrix.csv", False, False)
#get_paoh_edges("matariki-outlier-removed-matrix.csv", True, True)
get_paoh_edges("matariki-outlier-removed-matrix.csv", False, False)

get_hyperedge_counts("relationships_aggregated.csv", "relationships_aggregated2.csv")
get_hyperedge_counts("relationships_years.csv", "relationships_years2.csv")
#encode_paoh_weights("relationships_weights_adjusted.csv")

#props = ["freq_band"]
for prop in props:
    maximum = generate_aggregated_hypergraph("matariki-outlier-removed-matrix.csv",True,False,prop)     
    update_file("result2_" + prop + ".csv", maximum, prop)

##########################################################################       

#compute_metric("sets_without_maori.csv", "relationships_years2.csv", "triggers.csv")
##Merge the resulting sheets using vertical lookup  
#merge_files("2-metrics.csv", "2-metrics2.csv", "2-metrics3.csv", "2-metrics-final-new.csv")

###########################################################################       

print("Done!")