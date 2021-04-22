# -*- coding: utf-8 -*-
import pandas as pa
import re

"""This script contains functions for cleaning the RMT Corpus"""

#Rearranges tweets into alphabetical order.
#Useful for checking for duplicate/similar tweets in Google Sheets.
def order_alphabetically(input_file, output_file):
    #Read tweets from file
    tweets = pa.read_csv(input_file, sep="\t")
    #Remove all instances of <link> and <user>
    tweets['content'] = tweets['content'].str.replace("<user>","")
    tweets['content'] = tweets['content'].str.replace("<link>","")
    #Replace multiple spaces with single space
    tweets["content"] = tweets["content"].apply(lambda x: re.sub(" {2,}"," ", x))
    #Remove leading spaces
    tweets["content"] = tweets["content"].apply(lambda x: re.sub("^ {1,}","", x))
    #Remove trailing spaces
    tweets["content"] = tweets["content"].apply(lambda x: re.sub(" {1,}$","", x))
    tweets = tweets.sort_values(by ='content')
    tweets.to_csv(output_file, sep="\t", header = True, index = False)

#Saves all duplicate tweets in a file.
#Does this by looking for multiple instances of the same tweet id.
def get_duplicates(input_file):
    #Read tweets from file
    tweets = pa.read_csv(input_file, sep="\t")
    #Extract duplicate tweets
    duplicate_tweets = tweets[tweets.duplicated(subset='id', keep=False)]
    #Print out number of duplicate tweets
    print("Duplicates:", len(duplicate_tweets))
    #For UNIQUE duplicates (i.e. one of each)
    #duplicate_tweets = tweets[tweets.duplicated(subset='id', keep="first")]
    duplicate_tweets.to_csv("duplicate-tweets-downloaded.csv", sep="\t", index=False) 

#Removes all duplicates except the first instance.
def remove_duplicates(input_file):
    tweets = pa.read_csv(input_file, sep="\t")
    #If some IDs have speechmarks on the end and others do not, need to make
    #sure they are consistent
    #tweets["id"] = tweets["id"].astype(str).apply(lambda x: re.sub("^'","", x))
    #tweets["user.id"] = tweets["user.id"].astype(str).apply(lambda x: re.sub("^'","", x))
    #tweets["conversationId"] = tweets["conversationId"].astype(str).apply(lambda x: re.sub("^'","", x))    
    print("Original size:", len(tweets))
    #print(tweets['id'])
    unique_tweets = tweets.drop_duplicates(subset='id', keep="first")
    print("New size:", len(unique_tweets))
    unique_tweets.to_csv("bilingual-tweets-all-good.csv", sep="\t", index=False)

#Find IDs that occur in one file but not the other.
def get_unique_tweets_from_file(input_file, input_file2):   
    ids = pa.read_csv(input_file, sep="\t")
    original = set(ids['id'].tolist())
    print("Original number of IDs:", len(original))
    ids2 = pa.read_csv(input_file2, sep="\t")
    new = set(ids2['id'].tolist()) 
    print("New number of IDs:", len(new))
    extras = original - new
    print(len(extras))
    print(list(extras))

#############################################################################
#REMOVE TWEETS
    
#Removes all tweets from the account "UC_Poesias_Bot".
#If we wanted to remove data from multiple users, could iterate list of users.
def remove_bot(input_file, output_file):
    tweets = pa.read_csv(input_file, sep="\t")
    print("Original size:", len(tweets))
    #Remove Maori bible tweets
    user = "UC_Poesias_Bot"    
    print(str(user) + ": " + str(len(tweets[tweets['user.username'] == user])))
    tweets = tweets[tweets['user.username'] != user]
    tweets.to_csv(output_file, sep="\t", index = False) 
    print("New size:", len(tweets))
    
#Removes tweets with the specified tweet or user ids.
#"field" parameter can be "id" (for tweet ids) or "user_id"
#"ids" parameter is the list of tweet ids or user ids
def remove_tweets_by_id(input_file, output_file, field, ids):
    tweets = pa.read_csv(input_file, sep="\t")
    print("Original size: ", len(tweets))
    tweets_to_remove = ids
    print("Tweets to remove: ", len(ids))
    #UPDATE CODE TO GET USERNAMES THAT CORRESPOND WITH THE ABOVE IDS
    for tweet in tweets_to_remove:
        #THis will always be 1 if tweet id (but may be >1 if user id)
        print(str(tweet) + ": " + str(len(tweets[tweets[field] == tweet])))
        tweets = tweets[tweets[field] != tweet]
    tweets.to_csv(output_file, sep="\t", index = False) 
    print("New size: ", len(tweets))
        
#Removes tweets containing less than four words.
def remove_short_tweets(input_file, output_file):
    tweets = pa.read_csv(input_file, sep="\t")
    print("Original size:", len(tweets))    
    print("Short tweets:", len(tweets[tweets['total_words'] <= 3]))    
    tweets = tweets[tweets['total_words'] > 3]
    tweets.to_csv(output_file, sep="\t", index = False) 
    print("New size:", len(tweets))

#Removes similar tweets (from the same user only).
def remove_similar_tweets(input_file):
    tweets = pa.read_csv(input_file, sep="\t", lineterminator='\n')        
    #Create copy of dataframe to preserve original formatting
    original = tweets.copy(deep=True)
    #Loop through all users in the dataframe
    for user in tweets['user.id'].unique():
        print(user)
        #Select all tweets by the current user that contain six words or more
        user_tweets = tweets[(tweets['user.id'] == user) & (tweets['total_words']>6)]
        #print(user_tweets)   
        #Lower-case all text
        current_user = user_tweets.copy(deep=True)
        current_user['content'] = current_user['content'].str.lower()
        current_user['content'] = current_user['content'].str.replace("<user>","")
        current_user['content'] = current_user['content'].str.replace("<link>", "")
        current_user['content'] = current_user['content'].str.replace("\d","")
        current_user['content'] = current_user['content'].str.replace('[^\w\s]','')
        current_user['content'] = current_user['content'].str.replace('\s+','')
        #print(current_user)
        #Remove any duplicate tweets (retain first instance)       
        current_user.drop_duplicates(subset = 'content', keep = "first", inplace = True)         

        #Select all tweets containing fewer than six words        
        short_tweets = tweets[(tweets['user.id'] == user) & (tweets['total_words']<=6)]

        #Merge the two dataframes (for tweets with diff. lengths) with the original                 
        merged = original[original.index.isin(current_user.index)]
        merged2 = original[original.index.isin(short_tweets.index)]        
        #df1 = merged.set_index('id').combine_first(merged2.set_index('id')) #use index = True
        df1 = merged.combine_first(merged2)
#        if(user=="nan"): #Use is_null() method instead
#            user="000'"
        df1.to_csv(str(user) + "-similar-tweets-removed.csv", sep="\t", header = False, index = False)

#Removes similar tweets (among same AND different users).
#I didn't end up using this!
def remove_all_similar_tweets(input_file):
    tweets = pa.read_csv(input_file, sep="\t")    
    #Create copy of dataframe to preserve original formatting
    original = tweets.copy(deep=True)
    tweets['content'] = tweets['content'].str.lower()
    tweets['content'] = tweets['content'].str.replace("<user>","")
    tweets['content'] = tweets['content'].str.replace("<link>","")
    tweets['content'] = tweets['content'].str.replace("\d","")
    tweets['content'] = tweets['content'].str.replace('[^\w\s]','')
    tweets['content'] = tweets['content'].str.replace('\s+','')
    #tweets.to_csv('test.csv', header=False, index=True)
    duplicates = tweets[tweets['content'].duplicated(keep=False)]
    #print(duplicates)
    duplicates.to_csv("duplicates.csv", sep="\t", header = True, index = False)
    tweets.drop_duplicates(subset = 'content', keep = "first", inplace = True)    
    #Merge tweets with copy
    merged = original[original.index.isin(tweets.index)]    
    return merged

#STEP 4: Remove formulaic tweets by searching for certain strings by certain users
def remove_others(input_file, output_file):
    tweets = pa.read_csv(input_file, sep="\t")
    print("Original size:", len(tweets))
    tweets = tweets[~tweets['content'].str.contains("2nd", flags=re.IGNORECASE)]
    print("After removing all tweets with '2nd:'", len(tweets))
    tweets = tweets[~tweets['content'].str.contains("PŪKANA - TE MANA KURATAHI 2013", flags=re.IGNORECASE)]
    print("After removing Pūkana:", len(tweets))
    #Remove tweets by TeAo_Official that contain...
    tweets.drop(tweets[(tweets['user.username'] == "TeAo_Official") & (tweets['content'].str.contains("RESULTS", flags=re.IGNORECASE))].index, inplace=True)
    unwanted_strings = ["2016 Te Hui Ahurei o Tūhoe -", 
                        "2018 Mātaatua Kapa Haka Regional Aggregate", 
                        "2019 TE MATATINI KI TE AO DRAW", 
                        "Aggregate - TE REO","Aotea Senior Kapa Haka Regionals -",
                        "HAKA TAPARAHI:","2016 Te Hui Ahurei o Tūhoe -",
                        "Mataatua Kapa Haka Regionals -",
                        "Ngā Manu Korero",
                        "Non-aggregate KĀKAHU",
                        "Rangitāne Tangata Rau Kapa Haka Festival",
                        "TE MATATINI - AGGREGATE",
                        "Tai Tokerau Maranga Mai E Te Iwi",
                        "TE REO: ",
                        "Tainui Waka Kapa Haka Festival ",
                        "Tairāwhiti Senior Tamararo Regionals -",
                        "Te Arawa Kapa Haka Regionals",
                        "Te Arawa Senior Kapa Haka Regionals -",
                        "Te Haaro o Te Kaahu Kapa Haka Kura Tuarua 2016",
                        "Te Kura Wiwini, Te Kura Wawana",
                        "Te Kura Wīwini, Te Kura Wāwana",
                        "Te Matatini 2015 -",
                        "Tāmaki Makaurau Senior Kapa Haka Regionals -",
                        "Waitaha Senior Kapa Haka Competition -"]
    for string in unwanted_strings:    
        tweets.drop(tweets[(tweets['user.username'] == "TeAo_Official") & (tweets['content'].str.contains(string))].index, inplace=True)    
    print("After removing TeAo_Official:", len(tweets))
    tweets.drop(tweets[(tweets['user.username'] == "HURIMOZ") & (tweets['content'].str.contains("10 ngā tāera whakaputa Tohu Whaimana Poronīhiana"))].index, inplace=True)
    tweets.drop(tweets[(tweets['user.username'] == "TumekeFM") & (tweets['content'].str.contains("Ae i roa te wā, heoi i tutuki."))].index, inplace=True)
    tweets.drop(tweets[(tweets['user.username'] == "kupumaorinz") & (tweets['content'].str.contains(":"))].index, inplace=True)
    tweets.drop(tweets[(tweets['user.username'] == "TeIpukarea") & (tweets['content'].str.contains("via"))].index, inplace=True)
    print("After removing the rest:", len(tweets))
    #Save to file
    tweets.to_csv(output_file, sep="\t", index = False) 

#############################################################################

#GET EXTRA METADATA 
    
#Get IDs for tweets that need looking up via Twitter APA.
def get_ids_for_api(input_file, input_file2, output_file):
    all_ids = pa.read_csv(input_file, sep="\t")
    ids = all_ids['id'].tolist()
    ids_retrieved = pa.read_csv(input_file2, sep="\t")
    ids_to_remove = ids_retrieved['id'].tolist()
    ids_to_retrieve = set(ids) - set(ids_to_remove)
    print(len(ids_to_retrieve))
    with open("ids2.csv", 'w', encoding="utf8") as f:
        print("id", file=f)
        for tid in ids_to_retrieve:
            print(tid, file=f)
    f.close()
      
#Adds newly-retrieved data to original dataframe
def add_apa_data(input_file, input_file2, output_file):
    tweets = pa.read_csv(input_file, sep="\t")
    apa_data_to_add = pa.read_csv(input_file2, sep="\t")
    #Calculate favourites
    apa_data_to_add['favourites'] = apa_data_to_add['likeCount'] + apa_data_to_add['retweetCount'] + apa_data_to_add['quoteCount']      
    #apa_data_to_add["user.id"] = apa_data_to_add["user.id"].apply(str) + "'"
    #apa_data_to_add["conversation_id"] = apa_data_to_add["conversation_id"].apply(str) + "'"
    #apa_data_to_add["in_reply_to_user_id"] = apa_data_to_add["in_reply_to_user_id"].apply(str) + "'"  
    #https://stackoverflow.com/questions/24768657/replace-column-values-based-on-another-dataframe-python-pandas-better-way
    tweets = tweets.set_index('id')
    apa_data_to_add = apa_data_to_add.set_index('id')
    tweets.update(apa_data_to_add)
    tweets.reset_index(inplace=True)    
    tweets.to_csv(output_file, sep="\t", index = False)
    
def get_unique_ids_from_apa_data(input_file, output_file):
    tweets = pa.read_csv(input_file, sep="\t")
    tweets = tweets[['user.username','user.displayname','user.id','user.description','user.descriptionUrls','user.verified','user.created','user.followersCount','user.friendsCount','user.statusesCount','user.favouritesCount','user.listedCount','user.mediaCount','user.location','user.linkUrl','user.linkTcourl','user.url']]
    tweets.drop_duplicates(subset = 'user.username', keep = "first", inplace = True)   
    tweets.to_csv(output_file, sep="\t", index = False)

def add_user_info(file1, file2, file3, joinCol):
    df1 = pa.read_csv(file1, sep="\t", dtype={'id': 'str'}) 
    #del df1['user.username'] 
    #del df1['user.numTweets']
    df2 = pa.read_csv(file2, sep="\t", dtype={'id': 'str'}) 
    df3 = pa.merge(df1,df2,on=joinCol, how="outer")
    #df3 = df3.sort_values(by='date')
    df3.to_csv(file3, sep="\t", index=False)

#############################################################################
#TIDY UP CORPUS - SORT TWEETS AND CALCULATE DERIVED ATTRIBUTES

def sort_by_date(input_file, output_file):
    tweets = pa.read_csv(input_file, sep="\t")
    tweets = tweets.sort_values(by='date')
    tweets.to_csv(output_file, sep="\t", index=False)

#Calculates the number of tweets per user in the corpus & adds this as a column.
def tweets_per_user(input_file, output_file):
    tweets = pa.read_csv(input_file, sep="\t")
    #user_counts = tweets["user.username"].value_counts()
    #user_counts.to_csv(output_file, header=False, index=True)
    #Add frequency back to original dataframe
    #https://stackoverflow.com/questions/22391433/count-the-frequency-that-a-value-occurs-in-a-dataframe-column/22391554
    tweets['user.numTweets'] = tweets.groupby('user.id')['user.id'].transform('count')
    #tweets.drop_duplicates(subset = 'user.id', keep = "first", inplace = True)
    #tweets = tweets[['user.username','user.alias','user.numTweets']]
    tweets.to_csv(output_file, header=True, index=False, sep="\t")

#Extracts the year from timestamp of each tweet.
def get_year(input_file, output_file):
    tweets = pa.read_csv(input_file, sep="\t")
    #Delete existing column - missing values...
    del tweets['year']    
    #There are three date formats:
    #1) 2009-08-08T03:01:10.000Z
    #2) 2009-03-28T19:05:52+00:00
    #3) 2011-03-10T9:43PM
    #In all cases, the year is the first four digits...
    #Extract year from timestamp
    #https://stackoverflow.com/questions/13682044/remove-unwanted-parts-from-strings-in-a-column
    tweets['year'] = tweets['date'].str.extract(r'(^\d{4})', expand=False)
    tweets['year'] = tweets['year'].fillna("Unknown")
    #print(tweets)
    #Save df with 'year' column
    tweets.to_csv(output_file, header=True, index=False, sep="\t")

def fix_gender_and_year(input_file, output_file):
    tweets = pa.read_csv(input_file, sep="\t")
    #Populate ALL empty cells with "Unknown"
    tweets = tweets.fillna("Unknown")    
    #Standardise gender values
    tweets.loc[(tweets['gender'] == 'unk'),'gender']='Unknown'
    tweets.loc[(tweets['gender'] == 'm'),'gender']='male'
    tweets.loc[(tweets['gender'] == 'f'),'gender']='female'
    #Change null years to 0 (for loading into RAW Graphs)
    tweets.loc[(tweets['year'] == 'Unknown'),'year']=0
    #Save to CSV
    tweets.to_csv(output_file, sep="\t", index=False)            

def fix_account_status(input_file, output_file):
    tweets = pa.read_csv(input_file, sep="\t")
    tweets.rename(columns = {'user.error' : 'user.status'}, inplace = True)
    #df.loc[df['user.protected' == True, 'FirstName'] = "Matt"
    tweets.loc[(tweets['user.protected'] == True),'user.status']='protected'
    del tweets['user.protected']
    tweets.to_csv(output_file, sep="\t", index=False)                

def get_missing_ids(input_file1, input_file2):
    tweets = pa.read_csv(input_file1, sep="\t")
    users = pa.read_csv(input_file2, sep="\t")
    tweets = set(tweets['user.id'].tolist())
    print(len(tweets))
    users = set(users['user.id'].tolist())
    print(len(users))
    missing_users = set(tweets - users)
    print(missing_users)

def remove_null_ids(input_file, output_file1, output_file2):
    tweets = pa.read_csv(input_file, sep="\t")
    good_ids = tweets.loc[~tweets['id'].isna()]
    print(len(tweets))
    null_ids = tweets.loc[tweets['id'].isna()]
    good_ids.to_csv(output_file1, sep="\t", index=False)                
    null_ids.to_csv(output_file2, sep="\t", index=False)                
    
def add_favourites(input_file, output_file):
    tweets = pa.read_csv(input_file, sep="\t")
    tweets['favourites'] = tweets['likeCount'] + tweets['retweetCount'] + tweets['quoteCount']      
    tweets.to_csv(output_file, sep="\t", index=False)        
    
def check(input_file):
    tweets = pa.read_csv(input_file, sep="\t")
    years = tweets.loc[tweets['year'] != "Unknown"]
    print("Years:", len(years))
    timestamps = tweets.loc[~tweets['date'].isna()]
    print("Timestamps:", len(timestamps))    
    favourites = tweets.loc[~tweets['favourites'].isna()]
    print("Favourites:", len(favourites))
    likes = tweets.loc[~tweets['likeCount'].isna()]
    print("Likes:", len(likes))
          
def get_num_cols(input_file):
    tweets = pa.read_csv(input_file, sep="\t")
    print(len(list(tweets.columns)))

#[] is like "None" (different from missing/unknown)
def clean_data(input_file, output_file):
    tweets = pa.read_csv(input_file, sep="\t")
    #print(tweets['user.id'])
    tweets.loc[tweets['user.id'] == "315453674'", 'user.ethnicity'] = "Pākehā"
    tweets.loc[(tweets['user.gender'] == 'unknown'),'user.gender']='Unknown'    
    tweets.loc[(tweets['error'].isna()),'error']='None'
    #If outlinks is not null (i.e. has [] or ['http://...']), set media = [], but ONLY if meda is currently NULL!
    tweets.loc[(tweets['media'].isna() & ~tweets['outlinks'].isna()),'media']='[]'
    #If media is null and tweet does not contain <link>, change to "[]" 
    #Because if the tweet does not have a <link>, there can't be any media
    tweets.loc[(tweets['media'].isna() & ~tweets['content'].str.contains("<link>")),'media']='[]'
    #If outlinks is null and tweet does not contain <link>, change to "[]"
    #Otherwise, "Unknown" (because link is not known, although we could possibly find it in original APA JSON data)
    tweets.loc[(tweets['outlinks'].isna() & ~tweets['content'].str.contains("<link>")),'outlinks']='[]'
    #If URL is blank, generate URL
    tweets.loc[(tweets['url'].isna()),'url']='https://twitter.com/' + tweets['user.username'] + "/status/" + tweets['id'].astype(str).apply(lambda x: re.sub("'","", x))
    #user.iwi - could put N/A if not "Māori", but there may be other Māori users...    
    #Haven't really TESTED this properly...
    tweets.loc[(tweets['user.linkTcourl'].isna() & ~tweets['user.description'].isna()),'user.linkTcourl']='None'
    tweets.loc[(tweets['user.linkUrl'].isna() & ~tweets['user.description'].isna()),'user.linkUrl']='None'
    tweets.loc[(tweets['user.description'].isna() & ~tweets['user.link'].isna()),'user.description']='[]'
    tweets.loc[(tweets['user.descriptionUrls'].isna() & tweets['user.description'] == "[]"),'user.descriptionUrls']='[]'
    tweets.loc[(tweets['user.link'].isna()),'user.link']='https://twitter.com/' + tweets['user.username']
    #Populate ALL remaning null values (for all columns) with "Unknown"    
    tweets = tweets.fillna("Unknown")    
    #Find columns with blank values
    cols = list(tweets.columns)
    print("Variables with blank values")
    for col in cols: 
        null_tweets = tweets.loc[tweets[col].isna()]
        if(len(null_tweets) > 0):
            print(col)    
#    print("Unique values:")
#    for col in cols:
#        if(col not in ['id','content','user.id','user.alias','user.username','user.displayname','maori_words','user.description','conversationId','in_reply_to_user_id','user.profileBannerUrl','user.profileImageUrl']):
#            distinct_values = sorted(tweets[col].astype(str).unique())
#            print(col, distinct_values)
#            print("")
    tweets.to_csv(output_file, sep="\t", index=False)  
    
    #CODE FOR CREATING MISSING VALUES VISUALISATION
    #Generate matrix of present/absent data           
    for col in cols:
        tweets.loc[tweets[col] != 'Unknown',col]=1
        tweets.loc[(tweets[col] == 'Unknown'),col]=0    
    tweets["num_variables"] = tweets.sum(axis=1)
    tweets.to_csv("missing-values-matrix.csv", sep="\t", index=False)      
    #Compute the number of duplicate rows
    #https://stackoverflow.com/questions/35584085/how-to-count-duplicate-rows-in-pandas-dataframe
    tweets = tweets.groupby(tweets.columns.tolist(),as_index=False).size()
    #del tweets['sum']
    tweets.to_csv("missing-values-matrix-agg-row.csv", sep="\t", index=True, header=True)

##############################################################################

#cols = list of columns, col_names = list of names for those cols (in same order)
#e.g. cols = ['id','content','conversationId','date','error','favourites','in_reply_to_user_id','lang','likeCount','maori_words','media','num_maori_words','outlinks','percent_maori','quoteCount','replyCount','retweetCount','sourceLabel','total_words','url','user.id','year']
def get_subset(input_file, output_file, cols, col_names):
    tweets = pa.read_csv(input_file, sep="\t")
    tweets = tweets[cols]
    tweets.columns = col_names
    tweets.to_csv(output_file, sep="\t", index = False)
 
def extract_user_info(input_file, output_file):
    tweets = pa.read_csv(input_file, sep="\t")
    #Extract all user data
    #Could just serach for cols that start with "user."    
    users = tweets[['user.id','user.username','user.alias','user.displayname','user.location','user.region','user.gender','user.ethnicity','user.iwi','user.created','user.description','user.descriptionUrls','user.status','user.favouritesCount','user.followersCount','user.friendsCount','user.link','user.linkTcourl','user.linkUrl','user.listedCount','user.mediaCount','user.profileBannerUrl','user.profileImageUrl','user.statusesCount','user.verified','user.numTweets']]
    users.columns = ['user.id','user.username','user.alias','user.display_name','user.location','user.region','user.gender','user.ethnicity','user.iwi','user.created','user.description','user.description_urls','user.status','user.favourites_count','user.followers_count','user.friends_count','user.link','user.link_tcourl','user.link_url','user.listed_count','user.media_count','user.profile_banner_url','user.profile_image_url','user.statuses_count','user.verified','user.num_tweets']
    users.drop_duplicates(subset = 'user.id', keep = "first", inplace = True)   
    users.to_csv(output_file, sep="\t", index = False)

#METHOD CALLS HERE
get_subset("sorted23.csv", "rmt-corpus-v1.csv", ["ids"], ["ids"])
print("Done!")