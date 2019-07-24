import csv
import os
import re
import pandas as pa
from twokenize import tokenizeRawTweetText

#Get the current directory
DIR = os.path.dirname(os.path.realpath(__file__))
#NB: Directory needs to be empty apart from this Python file and CSVs to run it on!
#CSVs should be called <loanword>.csv with no space or macrons (e.g. "maori.csv")

#When merging multiple files, header of next file appends to same line as last tweet of previous file
#This method corrects this by moving the header down a line. 
def fix_merge_issue(inputFile):
    goodTweets = []
    with open(inputFile, 'r') as f:
        for line in f:
            #Correct merge issue - split last line of previous file from first line of next file
            line = line.replace("username;date;retweets", "\nusername;date;retweets")
            goodTweets.append(line)
    #Write to same file
    outputFile = inputFile
    with open(outputFile, 'w') as f:
        for tweet in goodTweets:
            f.write(tweet)
    print("Merge issue fixed")
                        
#Converts raw data (with semi-colon separated tweets) to TSV file 
#Cleans tweets by removing retweets (marked with 'rt'), blank lines and tweets where username contains target loanword (e.g. @kiwi, @happy_kiwi).
def cleanTweets(inputFile):
    goodTweets = []
    #Insert tab-separated header
    goodTweets.append("username\tdate\tretweets\tfavourites\ttext\tgeo\tmentions\thashtags\tid\tpermalink\n")
    #Read file
    with open(inputFile, 'r') as f:
        for line in f:
            #Convert data to lowercase
            line2 = line.lower().replace(";", " ;")
            #Extract loanword from filepath
            word = inputFile.replace(DIR + "/", "").replace(".csv", "")
            #Regular expression to find users whose username contains a loanword (e.g. @happy_kiwi) 
            #Need to fix: If word has a macron, does not look for macron version
            #Fixed: If tweet contains a user mention and #loanword afterwards, discarded
            #e.g. miaangela;2018-12-30 01:06;1;3;"Top @edfringe show from @ModernMariQ Was expecting to be blown away by the singing and the humour but did not see the emotional story-telling coming and it had me Can’t recommend this enough, only 3 shows left #haeremai";;@edfringe @ModernMaoriQ;#haeremai;"1033002746243436545";https://twitter.com/miaangela/status/1078985508057886720
            username = re.compile('[@|_]\S*' + word.lower())            
            #Constant to store number of columns of data; this number minus one is the number of semi-colons we expect to read in
            NUM_COLUMNS = 10;
            #If tweet TEXT contains at least one semi-colon 
            if line.count(";") > (NUM_COLUMNS - 1):
                #Get number of semi-colons in tweet
                semicolonsInTweet = line2.count(";") - (NUM_COLUMNS - 1)
                #For each semi-colon in Tweet
                for i in range(semicolonsInTweet):
                    #Remove semi-colon from Tweet
                    line = replaceOccurrence(line, ";", ",", 4) 
            #Remove any tabs already in Tweet
            line = line.replace("\t", "")
            #Replace all (remaining) semi-colons with tab delimiter
            line = line.replace(";", "\t")
            #Remove retweets, blank lines and old-style headings
            if '"rt' not in line2 and "username ;date ;retweets" not in line2 and line2 != "\n": #and "<phrase>" not in line2
                #Remove tweets containing loanword in username
                #print(username.search(line2))
                if(username.search(line2) == None):
                    #Add all other tweets to list
                    goodTweets.append(line)
    #Write to file
    outputFile = DIR + "/" + word + "-duplicates.csv"    
    with open(outputFile, 'w') as f:
        for tweet in goodTweets:
            f.write(tweet)
                        
#Replaces the nth occurrence of the given substring.
#Copied from https://forums.cgsociety.org/t/python-how-to-replace-nth-occurence-of-substring/1562801/2 
def replaceOccurrence(str, search, replacement, index):
    split = str.split(search, index + 1)
    if len(split) <= index + 1:
        return str
    return search.join(split[:-1]) + replacement + split[-1]

#Removes tweets that contain fewer than five tokens (words).
def remove_short_tweets(inputFile):
    word = inputFile.replace(DIR + "/", "").replace("-duplicates.csv", "")
    #Read the given CSV
    tweets = pa.read_csv(inputFile, sep="\t")
    count = 0
    #For each tweet
    for tweet in tweets['text']:
        #Count number of tokens in tweet
        tokens = tokenizeRawTweetText(tweet.lower())
        #If there are fewer than five
        if(len(tokens)<5):
            #Remove tweet
           tweets = tweets.drop(tweets.index[count])
        #Otherwise, increase count
        else:
            count+=1
    print("Short tweets removed")
    #Save to output file
    outputFile = DIR + "/" + word + "-duplicates2.csv" 
    tweets.to_csv(outputFile, sep="\t", index = False)     

#Removes tweets that have different id's but identical or almost identical text (i.e. same wording but slightly different punctuation and/or spelling). 
def removeSimilarTweets(inputFile):
    #Extract loanword from filename
    word = inputFile.replace(DIR + "/", "").replace("-duplicates2.csv", "")
    #Make dataframe from CSV file
    tweets = pa.read_csv(inputFile, sep="\t")        
    #Avoid rounding id's when merging
    tweets['id'] = tweets['id'].apply("int64")
    #Create copy of dataframe to preserve original formatting
    original = tweets.copy(deep=True)
    #Drop successive duplicate (or near-duplicate) tweets
    #Remove (most) emojis
    #https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
    tweets['text'] = tweets['text'].str.replace("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+",'')
    #Remove all @user mentions for string comparison (lots of robots have same text but diff. @user mentions)
    tweets['text'] = tweets['text'].str.replace('\@\w+','')
    tweets['text'] = tweets['text'].str.replace('\@\w+','')
    #Remove all numbers - this is another way that robots distinguish tweets
    #e.g.  @Harry_Styles I loved when they danced HAKA + RAP are amazing lol I love them! #latindirectioner 12
    #      @Harry_Styles I loved when they danced HAKA + RAP are amazing lol I love them! #latindirectioner 14
    tweets['text'] = tweets['text'].str.replace('\d','')
    #Remove all punctuation and spaces - sometimes an extra space, full stop, etc.
    tweets['text'] = tweets['text'].str.replace('[^\w\s]','')
    tweets['text'] = tweets['text'].str.replace('\s+','')
    #tweets.to_csv('test.csv', header=False, index=True)
    tweets.drop_duplicates(subset = 'text', keep = "first", inplace = True)
    #Merge tweets with copy
    merged = original[original.index.isin(tweets.index)]    
    #Add loanword column
    goodLoanword = word
    #Look up "special" words (macrons/phrases/both) in dictionary
    formatted = {"maori":"māori","non-maori":"non-māori","pakeha":"pākehā","porangi":"pōrangi","haeremai":"haere mai","kiaora":"kia ora","kapahaka":"kapa haka","tenakoutou":"tēnā koutou","kiakaha":"kia kaha","kowhai":"kōwhai","whanau":"whānau","hangi":"hāngī","tereo":"te reo","kaimoana":"kai moana","tenakoe":"tēnā koe","korero":"kōrero","powhiri":"pōwhiri","morena":"mōrena","tangatawhenua":"tangata whenua","kakariki":"kākāriki","kohanga":"kōhanga","hapu":"hapū","kaumatua":"kaumātua","kainga":"kāinga","wahitapu":"wāhi tapu","wananga":"wānanga","hikoi":"hīkoi","papatuanuku":"papatūānuku","whangai":"whāngai","mawhero":"māwhero","hoha":"hōhā","kawanatanga":"kāwanatanga"}    
    for loanword in formatted:
        if word in formatted:
            goodLoanword = formatted.get(word, "none")
    merged.insert(0, 'loanword', goodLoanword)
    
    #Reorder columns
    #print(list(merged.columns.values))
    merged = merged[['loanword', 'id', 'text', 'username', 'date','retweets','favourites','geo','mentions','hashtags','permalink']]
    
    #Store in CSV
    outputFile = DIR + "/" + word + "-good.csv"
    #print(outputFile)
    merged.to_csv(outputFile, sep="\t", index = False) 
    #print(tweets)

#Get filepaths for all CSVs in directory
def getFiles(suffix, methodToCall):
    for root, dirs, files in os.walk(DIR, topdown=False):   
        #For each file
        for filename in files:
            #If it's a CSV (containing Tweets)
            if filename.endswith(suffix):
                #Join filename with path to get location
                filePath = os.path.join(root, filename)            
                print("Processing %s..." % filename)
                methodToCall(filePath)

def fix_merge_issues():
    getFiles(".csv", fix_merge_issue)  
                
def convertAllToTSV():
    getFiles(".csv", cleanTweets)        

def removeAllShortTweets():   
    getFiles("-duplicates.csv", remove_short_tweets)        

def removeAllSimilarTweets():   
    getFiles("-duplicates2.csv", removeSimilarTweets)        

#Reads a CSV file containing tweets
def readCSV(inputFile):
    tweets = []
    with open(inputFile) as csvFile:
        for row in csv.reader(csvFile, delimiter='\n'):
            #For each tweet
            for term in row:
                tweets.append(term)
    return tweets

#MAKE SURE THERE ARE NO OTHER IMPORTANT FILES IN THIS DIRECTORY!!
#https://www.tutorialspoint.com/How-to-delete-multiple-files-in-a-directory-in-Python
def removeTmpFiles():
    #Remove all CSV files except "-good.csv" (cleaned data)
    #Probably safer to change this so that it only removes <word>.csv and -duplicates(2) in case there are other important files in directory 
    pattern = "^((?!-good\.csv|.py).)*$"
    for root, dirs, files in os.walk(DIR, topdown=False):
        for file in filter(lambda x: re.match(pattern, x), files):
            os.remove(os.path.join(root, file))

fix_merge_issues()            
convertAllToTSV()
removeAllShortTweets()
removeAllSimilarTweets()
removeTmpFiles()
print("Done!")