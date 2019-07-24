#Converts the raw CSV data into an ARFF file (for use in Weka)
#Input file = concatenation of .csv files for all query words
import pandas as pa
import re
import shutil

#Remove all headers that occur due to concatenation
def remove_headers(inputFile):
    goodTweets = []
    header = "loanword\tid\ttext\tusername\tdate\tretweets\tfavourites\tgeo	mentions\thashtags\tpermalink\n"
    goodTweets.append(header)
    #Read file
    with open(inputFile, 'r') as f:
        for line in f:            
            if header not in line:
                goodTweets.append(line)
    #Write to file    
    with open("headers-removed.csv", 'w') as f:
        for tweet in goodTweets:
            f.write(tweet)

#Change from tab-separated to comma-separated
def change_delimiter(inputFile):
    #Read the given CSV
    tweets = pa.read_csv(inputFile, sep="\t")
    #ARFF Format: id,username,timestamp,loanword,tweet,relevance
    #Remove additional columns
    tweets = tweets[['id','username','date','loanword','text']]
    #Save to output file
    outputFile = "comma-separated.csv"
    tweets.to_csv(outputFile, sep=",", index = False)

def convert_to_arff(inputFile):
    goodTweets = []
    #Read file
    with open(inputFile, 'r') as f:
        #Ignore header
        next(f)
        for line in f:
            #Add question mark to end of each line
            line = line.strip() + ',?\n'
            #Change all double quotes to singles
            for i in range(30):
                line = line.replace("“", "'")
                line = line.replace("”", "'")
                line = line.replace('"', "'")
                line = line.replace("''", "'") 
            #Remove single quote (') from end of Tweet
            line = line.replace("',?", ',?')
            #Add sppechmark to end of Tweet
            p = re.compile(r",[?]$")
            line = p.sub(r'",?', line)
            #Remove single quote (') from start of Tweet
            p = re.compile(r"(^\d*,[\S ^,]*,)'")
            line = p.sub(r"\1", line)
            #Add speechmark to start of username
            p = re.compile(r"(^\d*),")
            line = p.sub(r'\1,"', line)            
            #Add speechmark to end of username AND start of timestamp
            p = re.compile(r'(^\d*,"[^,]*),')
            line = p.sub(r'\1","', line)          
            #Add speechmark to end of timestamp AND start of loanword
            p = re.compile(r'(^\d*,"\S* \d\d:\d\d),')
            line = p.sub(r'\1","', line)                 
            #Add speechmark to end of loanword AND start of Tweet
            p = re.compile(r'(^\d*,"\S*","\S* \d\d:\d\d","[^,]*),')
            line = p.sub(r'\1","', line)                 
            goodTweets.append(line)
    #Close reader
    f.close()
    #Write to file
    outputFile = "crap.arff"    
    with open(outputFile, 'w') as f:
        for tweet in goodTweets:
            f.write(tweet)
    #Close writer
    f.close()

#Separate tweets with negative ids
def remove_bad_tweets(inputFile):
    goodTweets = []
    badTweets = []
    #Read file
    count = 0 
    with open(inputFile, 'r') as f:
        for line in f:
            p = re.search(r"-92233720", line)
            if p:
                count+=1
                badTweets.append(line)
            if not p:
                goodTweets.append(line)
    print(count)
    #Close reader
    f.close()
    #Write to file
    outputFile = "loanwords2.target.arff"    
    with open(outputFile, 'w') as f:
        for tweet in goodTweets:
            f.write(tweet)
    outputFile = "bad.target.arff"    
    with open(outputFile, 'w') as f:
        for tweet in badTweets:
            f.write(tweet)
    #Close writer
    f.close()

#Fix tweets with negative ids
def fix_negative_ids(inputFile):
    tweets = []
    with open(inputFile, 'r') as f:
        for line in f:
            bad_id = "-9223372036854775808"
            #print(line.count("\t"))
            
            #Replace bad id with good id                        
            good_id = re.search(r'(\d+)",\?$', line)
            good_id = good_id.group(1)
            #print(good_id)
            line = line.replace(bad_id, good_id)
            
            #Eliminate user mentions, hashtags and blank space at end of tweet
            post_tweet_text = re.search(r'\t\t.*$', line)
            post_tweet_text = post_tweet_text.group(0)
            #print(post_tweet_text)
            line = line.replace(post_tweet_text, ",?")
            
            #Remove single quote (') from end of Tweet
            line = line.replace("',?", ',?')
            #Add sppechmark to end of Tweet
            p = re.compile(r",[?]$")
            line = p.sub(r'",?', line)
            #Remove single quote (') from start of Tweet
            p = re.compile(r"(^\d*,[\S ^,]*,)'")
            line = p.sub(r"\1", line)
            #Add speechmark to start of username
            p = re.compile(r"(^\d*),")
            line = p.sub(r'\1,"', line)            
            #Add speechmark to end of username AND start of timestamp
            p = re.compile(r'(^\d*,"[^,]*),')
            line = p.sub(r'\1","', line)          
            #Add speechmark to end of timestamp AND start of loanword
            p = re.compile(r'(^\d*,"\S* \d\d:\d\d),')
            line = p.sub(r'\1","', line)                 
            #Add speechmark to end of loanword AND start of Tweet
            p = re.compile(r'(^\d*,"\S*","\S* \d\d:\d\d","[^,]*),')
            line = p.sub(r'\1","', line)                 

            tweets.append(line)
    #Write to file
    outputFile = "corrected-ids.arff"    
    with open(outputFile, 'w') as f:
        for tweet in tweets:
            f.write(tweet)
    #Close writer
    f.close()
    
#Merge positive ids with fixed ids
def merge_files(inputFile1, inputFile2):
    outputFile = "loanwords3.target.arff"
    with open(outputFile, "wb") as wfd:
        for f in [inputFile1, inputFile2]:
            with open(f, "rb") as fd:
                shutil.copyfileobj(fd, wfd, 1024*1024*10)
    print(inputFile1 + " and " + inputFile2 + " merged successfully!")
    
#Add ARFF structure and escape special characters with backslash
def escape_backslash(inputFile):
    goodTweets = []
    goodTweets.append("""@relation target-tweets
                      
@attribute id numeric
@attribute username string
@attribute timestamp date "yyyy-MM-dd HH:mm"
@attribute loanword string 
@attribute text string
@attribute relevance {relevant,non-relevant}

@data\n""")
    #Read file
    with open(inputFile, 'r') as f:
        for line in f:
            #If two blackslashes at end
            p = re.compile(r'[\\][\\]+",[?]$')
            line = p.sub(r'\\",?', line)
            p2 = re.compile(r'\\",[?]$')
            line = p2.sub(r'\\\",?', line)
            goodTweets.append(line)
    #Close reader
    f.close()
    #Write to file
    outputFile = "loanwords.target.arff"    
    with open(outputFile, 'w') as f:
        for tweet in goodTweets:
            f.write(tweet)
    #Close writer
    f.close()

#Run all methods in turn
#Input file is output of previous method (hence could put all in one line)
remove_headers("all-tweets.csv")
change_delimiter("headers-removed.csv")
convert_to_arff("comma-separated.csv")
remove_bad_tweets("crap.arff")
fix_negative_ids("bad.target.arff")
merge_files("loanwords2.target.arff","corrected-ids.arff")
escape_backslash("loanwords3.target.arff")
print("Done!")