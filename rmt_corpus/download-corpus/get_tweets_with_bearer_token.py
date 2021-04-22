import requests
import os
import json
import pandas as pa
import math 
import re 
import time

#Hydrates the RMT Corpus in batches of 100 tweets by querying the tweet IDs
#Adapted from Twitter's API v2 sample code: 
#https://github.com/twitterdev/Twitter-API-v2-sample-code

#To set your enviornment variables in your terminal run the following line:
#export 'BEARER_TOKEN'='<your_bearer_token>'

def auth():
    return os.environ.get("BEARER_TOKEN")

def create_url(tweet_ids):
    # Tweet fields are adjustable
    tweet_fields = "tweet.fields=text,conversation_id,in_reply_to_user_id,author_id,created_at,lang,source"
    # Other options include:
    # attachments, context_annotations, entities, non_public_metrics, geo,
    # organic_metrics, possibly_sensitive, promoted_metrics, public_metrics, 
    #referenced_tweets & withheld
    # Additional user data is also available
    #tweet_ids is a list of up to 100 tweet IDs 
    ids = 'ids=' + ",".join(tweet_ids)
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    return url

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers, batch_num):
    response = requests.request("GET", url, headers=headers)
    print("Batch {}, Code {}".format(batch_num,response.status_code))
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def segment_tweet_ids(input_file, BATCH_SIZE):
    tweets = pa.read_csv(input_file, sep="\t")
    ids = tweets['id'].astype(str).apply(lambda x: re.sub("'","", x))
    ids = ids.tolist()
    #batches = 1
    batches = []
    num_batches = math.ceil(len(ids) / BATCH_SIZE)
    for i in range(0, num_batches):
        #batch_num = str(i+1)
        #print(batch_num)     
        start = i*BATCH_SIZE
        end = (i*BATCH_SIZE+BATCH_SIZE)
        if end > len(ids):
            end = len(ids)
        curr_batch = ids[start:end] 
        batches.append(curr_batch)
    return batches

def main():
    bearer_token = auth()
    tweet_ids = segment_tweet_ids("rmt-corpus-v1.csv", 100)
    count = 0
    #300 queries per 15-minute window - edit as required
    RATE_LIMIT = 300
    for batch in tweet_ids:
        #To prevent rate limit being exceeded
        if(count != 0 and count % RATE_LIMIT == 0):
            #print("Sleeping for 15 minutes...")
            time.sleep(900)
        url = create_url(batch)
        headers = create_headers(bearer_token)
        json_response = connect_to_endpoint(url, headers, count+1)
        print(json.dumps(json_response, indent=4, sort_keys=True, ensure_ascii=False))
        count+=1
    
if __name__ == "__main__":
    main()