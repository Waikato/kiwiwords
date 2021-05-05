# Māori Twitter Corpus
The *Reo Māori Twitter (RMT) Corpus* is a collection of 79,018 te reo Māori tweets, designed for linguistic analysis and to help in the development of new Natural Language Processing (NLP) resources for the Māori community. The corpus captures output from 2,302 users, including a mixture of personal and institutional accounts. These users were identified via Prof. Kevin Scannell's [Indigenous Tweets website](http://indigenoustweets.com/mi/).

### Download the RMT Corpus
The tweets and user metadata in the RMT Corpus can be hydrated (downloaded from Twitter) using the code provided. The source code is adapted from Twitter's [sample code](https://github.com/twitterdev/Twitter-API-v2-sample-code) for API v2 endpoints.

Note: Some tweets in the corpus are no longer publicly available and, as such, cannot be downloaded. **Please [email David Trye](mailto:dtrye@waikato.ac.nz) if you would like access to the complete dataset, including additional metadata mentioned in our paper.**

The speed at which you can download the corpus depends on the [rate limit](https://developer.twitter.com/en/docs/twitter-api/rate-limits) for your Twitter developer account (e.g. 300 or 900 requests per 15-minute window). If you exceed the allocated limit, a 429 'Too many requests' error will be returned.

- Apply for a [Twitter developer account](https://developer.twitter.com/en/apply-for-access) if you do not have one already.
- Ensure that [Python 3](https://www.python.org/downloads/) is installed on your machine. The code for hydrating the corpus uses `requests==2.24.0`, which in turn uses `requests-oauthlib==1.3.0`. You can install these packages as follows:
```
pip install requests
pip install requests-oauthlib
```
- Download and extract all files in the <a href="../pics/rmt-v1.zip">rmt-v1</a> folder. This folder contains a file called `rmt-corpus-v1.csv`, which has the tweet IDs and selected metadata, as well as two Python scripts for downloading and formatting the data (namely, `get_tweets_with_bearer_token.py` and `json_to_tsv.py`).

- Configure your API bearer token by running the following command in the terminal:
```
export 'BEARER_TOKEN'='<your_bearer_token>'
```
- Run `get_tweets_with_bearer_token.py` from the terminal. 
```
python get_tweets_with_bearer_token.py > output.json
```
This will download the corpus in batches of 100 tweets. If you use the default settings, the script will take roughly 45 minutes to run, as it will attempt to download 30,000 tweets (300 requests x 100 tweets) every 15 minutes. The resulting file, `output.json`, is only pseudo-JSON (each batch is separated by a line in the form "Batch `X`, Code `Y`", where `X` and `Y` are numbers). 

- Run `json_to_tsv.py` to convert the output file to TSV format. 
```
python json_to_tsv.py
```
This script will produce a file called `rmt-corpus-final.csv`, which you can then open in a spreadsheet application. Tweet text is formatted consistently (special characters are removed, any HTML is decoded, and user mentions and links are standardised). The tweets are also supplemented with metadata from the original `rmt-corpus-v1.csv` file. A description of the variables in each of the CSV files is given below.

### Data Description: rmt-corpus-v1.csv

The following information (where known) is supplied in `rmt-corpus-v1.csv`, even if the tweet is no longer available on Twitter.

| Data Column                       | Description |
| -------------                     | ------------- |
| id                                | Twitter's unique identifier for the tweet. You can search for a tweet online by visiting [twitter.com/user/status/XXX](twitter.com/user/status/XXX), where `XXX` is the tweet's ID.  |
| num_maori_words                   | The number of Māori words in the tweet.
| total_words                       | The total number of words in the tweet.
| percent_maori                     | The percentage of Māori text detected in the tweet (=`num_maori_words` / `total_words`\*100).
| favourites                        | The number of favourites (likes, retweets & quotes) that the given tweet received. |
| reply_count                       | The number of replies that the given tweet received.
| user.alias                        | An alias for the author of the tweet in the form T`X`, where `X` represents the user’s ranking based on their total number of tweets in the corpus (`user.num_tweets`). |
| user.status                       | The account status (as of Decemeber 2020) of the user who wrote the tweet: 'active', 'protected', 'suspended' or 'not found'.|
| user.followers                    | The user's number of followers (as of December 2020). |
| user.friends                      | The number of accounts that the user follows (as of December 2020). |
| user.num_tweets                   | The total number of tweets in the corpus that were written by this user. |
| user.region                       | The user's location, based on self-reported information. Where possible, the data has been aggregated into [New Zealand regions](https://en.wikipedia.org/wiki/Regions_of_New_Zealand) and names of foreign countries. |
| year								| The year the tweet was written (between 2007 and 2020). |

### Data Description: rmt-corpus-final.csv

If the tweet is still publicly available on Twitter, the following variables will appear alongside those mentioned above. Missing values are indicated with 'None':

| Data Column                       | Description |
| -------------                     | ------------- |
| text								| The tweet content, with consistent formatting applied (special characters stripped, user mentions and links standardised). |
| conversation_id                   | The ID for the conversation that the tweet is part of. |
| in_reply_to_user_id               | If the tweet is written in reply to another, this is the ID of the user who who wrote the original tweet. | 
| author_id                         | Twitter's unique identifier for the user who wrote the tweet. |
| created_at                        | The timestamp when the tweet was posted, in the format `YYYY-MM-DDTHH:mm:ss.000Z`. |
| lang                              | The two-letter code representing the language that the tweet was (erroneously) classified as (NOT Māori, as the API does not support te reo). |
| source                            | The device or third-party application from which the tweet was posted (e.g. 'Twitter Web Client', 'Twitter for iPhone').
| error								| The reason why the tweet could not be downloaded, if there was an error ('Authorization Error', 'Not Found Error', 'None'). | 

### Other Resources
- Code for cleaning and analysing the RMT Corpus is available on the [project GitHub repository](https://github.com/Waikato/kiwiwords/tree/master/rmt_corpus).
- You can <a href="../pics/rmt-v1-wordlist.csv">download a wordlist</a> with frequencies for all words and hashtags in the corpus.

### Citing the RMT Corpus
If you use the RMT corpus, please cite the following paper:

- 'Building a Corpus of Māori Language Tweets' by Trye et al. (full reference coming soon!).

### Team

- [David Trye](https://www.cs.waikato.ac.nz/~dgt12/)
- [Te Taka Keegan](https://www.cms.waikato.ac.nz/people/tetaka)
- [Paora Mato](https://www.waikato.ac.nz/staff-profiles/people/pmato)
- [Mark Apperley](https://www.cms.waikato.ac.nz/people/mapperle)
- [Tamahau Brown](https://www.linkedin.com/in/tamahau-brown-9287b7139/)

External Collaborators:

- [Te Hiku Media](https://tehiku.nz/te-hiku-tech/), NZ
- [Kevin Scannell](https://cs.slu.edu/~scannell/index.html), Saint Louis University, US

### Funding

We graciously acknowledge the generous support of:

- Ngā Pae o te Māramatanga
- The University of Waikato

The information on this page was last checked in April 2021. Please [let us know](mailto:dtrye@waikato.ac.nz) if you notice any errors in the code and/or instructions. 
As of 12 April 2021, 72,575 tweets (**91.85%** of the RMT Corpus) could be successfully downloaded from Twitter.
