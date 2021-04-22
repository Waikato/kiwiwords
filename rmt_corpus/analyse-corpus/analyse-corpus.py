# -*- coding: utf-8 -*-

"""Functions for analysing the corpus from both the tweet and user perspective."""

#import pandas as pa
import pandas as pa

def get_user_link_stats(input_file):
    tweets = pa.read_csv(input_file, sep="\t")
    #User stats
    total_users = tweets['content'].str.count("<user>").sum()
    print("Total user mentions:", total_users)
    users = tweets[tweets['content'].str.contains("<user>")]
    print("Tweets with one or more user mentions:", len(users))
    print("The percentage of tweets with one or more user mentions is:", round(len(users)/len(tweets)*100))
    #Link stats
    total_links = tweets['content'].str.count("<link>").sum()
    print("Total links:", total_links)
    links = tweets[tweets['content'].str.contains("<link>")]
    print("Tweets with one or more links:", len(links))
    print("The percentage of tweets with links is:", round(len(links)/len(tweets)*100))
        
def get_category_values(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    #Populate empty cells with "Unknown"
    tweets = tweets.fillna("Unknown")
    cols_of_interest = ["lang", "sourceLabel", "user.username", "user.verified", "gender"]
    for col in cols_of_interest:
        column = tweets[col].value_counts()
        column.to_csv("col-" + col + ".csv", header=False, index=True, sep="\t")
                
def get_active_users_per_year(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    tweets['year'] = tweets['year'].astype(str)
    #Get a list of all years featured in the corpus
    years = sorted(tweets['year'].unique())
    with open("users-per-year.csv", 'w', encoding="utf8") as writer:
        #For each year
        for year in years:
            #Isolate tweets from the given year
            year_tweets = tweets[tweets['year'].str.contains(year)]
            user_stats = year_tweets['user.id'].value_counts()
            agg_stats = len(user_stats.to_dict())
            #user_stats = user_stats.sum()
            print(year, agg_stats)
            print(year, agg_stats, file=writer)
            #Get the number of users for the given year
                            
def get_new_users_per_year(input_file):
    tweets = pa.read_csv(input_file, sep="\t")
    tweets['year'] = tweets['year'].astype(str)
    years = sorted(tweets['year'].unique())
    print(years)
    users_seen = []
    for year in years:
        current_year = tweets[tweets['year'].str.contains(year)]
        users_in_year = current_year['user.id'].unique()
        previous_length = len(users_seen) 
        for user in users_in_year:
            if(user not in users_seen):
                users_seen.append(user)
        new_users = len(users_seen) - previous_length
        print(year, new_users)
        #print(year)
        #print(users_in_year)
            
#Calculates the number of tweets per year
def get_tweets_per_year(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    #Exclude Temihinga    
    #tweets = tweets[~tweets['user.username'].str.contains("temihinga", na=False)]
    tweets['year'] = tweets['year'].astype(str)
    year_stats = tweets['year'].value_counts()
    year_stats.to_csv("year-stats.csv", header=False, index=True, sep="\t")
    #Now get tweets per year for top 10 users
    #Preferably format output so that rows are users and columns are years
    #Note that I haven't done this (would need to some merge df's on years)
    #First, extract the top 10 users into a list
    top10 = tweets.groupby('user.username')['user.username'].count().nlargest(10).keys()
    print(top10)
    with open("top10users.csv", 'w', encoding="utf8") as writer:
        #For each username in the list
        for user in top10:
            #print(user)
            #Get the number of tweets per year for that particular user
            user_tweets = tweets[tweets['user.username'].str.contains(user)]
            year_stats = user_tweets['year'].value_counts() 
            #year_stats = 
            print(user, file=writer)
            print(year_stats.to_string(), file=writer)
            #Check all values sum to corresponding user's numtweets    

#get_tweets_per_year("rmt-test.csv", "rmt-test2.csv")
#get_actibe_users_per_year("sorted22.csv")
print("Done!")