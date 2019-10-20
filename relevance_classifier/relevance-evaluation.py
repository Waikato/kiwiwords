#Relevance-classifier-evaluation
#Answers the question "how many tweets were polled/harvested by each query word"?
#Based on loanword attribute, NOT frequency
#Can run on mlt-corpus-all and mlt-corpus-rel to determine what proportion of tweets "made the cut".

import pandas as pa

loanword = []
    
def get_diachronic_stats(inputFile):
    table_rows = []
    table_rows.append("loanword\t2006\t2007\t2008\t2009\t2010\t2011\t2012\t2013\t2014\t2015\t2016\t2017\t2018\n")    

    tweets = pa.read_csv(inputFile, sep="\t")
    #tweets = tweets[['id','username','timestamp','loanword','text','predicted','prediction']]
    #tweets = tweets[(tweets['predicted'] == "1:relevant")]
    
    overall = get_year_counts(tweets)
    converted = (str(o) for o in overall)
    converted = '\t'.join(converted)
    table_rows.append("overall\t" + converted + "\n")        
    
    #print("Overall counts:")
    #print(overall)
    
    loanwords = dict(tweets['loanword'].value_counts())
    
    for l in loanwords:
        print(l)
        tweets2 = tweets[(tweets['loanword'] == l)]
        counts = get_year_counts(tweets2)
        converted = (str(c) for c in counts)
        converted = '\t'.join(converted)
        
        table_rows.append(str(l) + "\t" + converted + "\n")        
    #Write to file
    outputFile = "diachronic-mlt-rel.csv"    
    with open(outputFile, 'w') as f:
        for t in table_rows:
            f.write(t)
    
def get_year_counts(tweets):
    y_keys = ["2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018"]
    y_values = []
    index = 0
    for year in y_keys:
        count = len(tweets[tweets['timestamp'].str.contains(year)])
        y_values.insert(index, count)
        index+=1
    return y_values   
    #print("\n".join("{}\t{}".format(k, v) for k, v in year_counts.items())) 
    #Write to file
    
get_diachronic_stats("mlt-corpus-rel.csv")
print("Done!")

#1,179,447
