# Putunga Reo Māori Tīhau: The Reo Māori Twitter Corpus

### Te Reo Māori
Ko te *Putunga Reo Māori Tīhau (RMT)* nei he putunga o ngā tīhau 79,018 kua tuhia ki te reo Māori. He mea hanga hei tautoko i ngā mahi reo Māori -ā-waha o te rorohiko, hei rauemi hoki mō ngā iwi Māori puta noa i te motu. E 2,302 ngā kaituhi pīhau reo Māori nei, ko ētehi he whaiaro nō te tangata ake, ko ētehi he mea tuku nō te kamupene. Kua tautohua ngā kaituhi pīhau nei e te pae tukutuku a [Indigenous Tweets](http://indigenoustweets.com/mi/) nā Prof. Kevin Scannell.

#### Kia tikiake te putunga RMT
Nā tēneki waehere e taea ai te tikiake i ngā pīhau me ngā raraungameta. Kua hangaia te waehere nei mai i ngā waehere o Twitter arā te waehere tauira o API v2 endpoints.

Kia mōhio mai: kō ētehi o ngā tīhau kāore i reira ināianei, nō reira ka kore e taea te tikiake. **Tukua tētehi īmēra ki a [David Trye](mailto:dtrye@waikato.ac.nz) inā ka hiahiatia te katoa o te putunga RMT me ētehi raraungameta i tua atu, he raraungameta kua kōrerotia i tā mātou pepa.** 

Ka hāngai te tere o tāu tikiake ki tāu ake rate limit i tāu pūkete kaiwhanake o Twitter (arā, 300, 900 rānei ngā tono ki ia 15 meneti). Ki te whakapaua tāu tatau, ka puta mai te kōrero hē: 429 'Too many requests'.

- Tonoa tētehi [Pūkete Kaiwhanake o Twitter](https://developer.twitter.com/en/apply-for-access) inā kaore i a koe tētehi.
- Me matua noho a [Python 3](https://www.python.org/downloads/) ki tāu rorohiko. Ka whakamahia e te waehere tikiake i te `requests==2.24.0`, ā, ka whakamahia hoki te `requests-oauthlib==1.3.0`. Ka whēnei ngā tono hei utaina ēnei:
```
pip install requests
pip install requests-oauthlib
```
- Tikiake me te unu i ngā kōnae katoa i te kōpake <a href="../pics/rmt.zip">rmt</a>. Kei tēneki kōpaki tētehi kōnae ko `rmt-corpus-v1.csv` te ingoa, kei reira ngā tīhau IDs me ngā raraungameta. Kei reira hoki ngā waehere Python e rua mō te tikiake me te whakahōputu o ngā raraunga (arā, `get_tweets_with_bearer_token.py` me te `json_to_tsv.py`).
- Kia whakaritea ai tāu API bearer token me tuku atu tēnei tono:
```
export 'BEARER_TOKEN'='<your_bearer_token>'
```
- Whārere `get_tweets_with_bearer_token.py`.
```
python get_tweets_with_bearer_token.py > output.json
```
Nā reira, ka tikiake te 100 tīhau i ia tono, ā, nā ēnei whakaritenga ka āhua 45 meneti pea te roa. Ka whēnei te roa i te mea, ka 30,000 tīhau (300 tono x 100 tīhau) i ia 15 meneti. I te otinga ake ka rauikatia ki te kōnae output.json heoi anō he pseudo-JSON kē; ka motumotu ngā taupū ki tētehi rārangi e whēnei ana; "Batch X, Code Y", he nama te X me te Y.

- Whārere `json_to_tsv.py` kia whakawhiti ai te kōnae putunga ki te hōputu TSV.
```
python json_to_tsv.py
```

Ko te otinga o tēnei waehere ko te kōnae `rmt-corpus-final.csv`, he kōnae ka tūwheratia ki te tautono ripanga. Kua rite tahi te hōputu o ngā kōrero tīhau, arā ka tangohia ngā pūāhua motuhake, ka weteoro te HTML, ā, ka rite tahi te whakatakoto o ngā kōrero kaitīhau me ngā tūhononga. Ka tāpiritia hoki ngā raraungameta mai i te kōnae motuhake o `rmt-corpus-v1.csv`. Ki raro iho nei ka whakamārama atu ngā taurangi kei ngā kōnae CSV.

#### He Whakamārama Raraunga: rmt-corpus-v1.csv
Koia nei ngā māramatanga (inā e mōhio ana) kei te kōnae `rmt-corpus-v1.csv`, ahakoa kei a Twitter tonu te tīhau ake, kāore rānei.

| Taurangi                          | Whakamārama |
| -------------                     | ------------- |
| id                                | Te tautohu motuhake o Twitter mō tēnei tīhau. Ka taea te rapu tēnei tautohu ki [twitter.com/user/status/XXX](twitter.com/user/status/XXX), inā ko XXX te tīhau tautohu. |
| num_maori_words                   | E hia ngā kupu Māori ki te tīhau. |
| total_words                       | E hia te katoa o ngā kupu ki te tīhau. |
| percent_maori                     | Ko te paiheneti o ngā kupu Māori ki te tīhau (=`num_maori_words` / `total_words`\*100).
| favourites                        | E hia ngā pānga (likes, retweets & quotes) i whakapā atu ki tēnei tīhau. |
| reply_count                       | E hia ngā whakahoki kōrero ki tēnei tīhau. |
| user.alias                        | He ingoakē mō kaitīhau, ka hangaia i te T`X`, inā ko te `X` tōna tūranga i te tatau whānui o āna tīhau i te putunga katoa (`user.num_tweets`). |
| user.status                       | Te tūnga pūkete (i te Tīhema 2020) o te tangata nāna te tīhau i tuku: ka 'active', 'protected', 'suspended', 'not found' rānei. |
| user.followers                    | Tokohia āna apataki (i te Tīhema 2020). |
| user.friends                      | E hia ngā hoa ka whaia e ia (i te Tīhema 2020). |
| user.num_tweets                   | E hia ngā tīhau kua tukuna e ia. |
| user.region                       | Tōna wākāinga, e ai ki a ia. Inā i taea, i whakaritea ngā rohe nei ki  [New Zealand regions](https://en.wikipedia.org/wiki/Regions_of_New_Zealand) me ngā ingoa o ngā whenua ki tāwāhi. |
| year								| Te tau kua tukuna te tīhau (2007-2020).|

#### He Whakamārama Raraunga: rmt-corpus-final.csv
Ki te ora tonu te tīhau ki a Twitter, ka tāpiri atu hoki ngā taurangi ki raro iho nei. Ki te kore te taurangi e kitea ka tuhia ‘None’.

| Taurangi                          | Whakamārama |
| -------------                     | ------------- |
| content								| Ko ngā kōrero o te tīhau; kua rite tahi te hōputu o nga kōrero tīhau, arā ka tangohia ngā pūāhua motuhake, ka weteoro te HTML, ā, ka rite tahi te whakatakoto o ngā kōrero kaitīhau me ngā tūhononga. |
| conversation_id                   | Ko te tautohu motuhake mō te kōrerorero e noho atu ai tēnei tīhau. |
| in_reply_to_user_id               | Mehemea he whakahoki kōrero tēnei ki te tīhau o tāngata kē, koia nei te tautohu motuhake o te tangata nāna te tīhau tuatahi i tuku. | 
| author_id                         | Ko te tautohu motuhake o Twitter mō te kaituhi o te tīhau. |
| created_at                        | Te wā me te rā i tuku ai te tīhau, ka whēnei te hōputu: `YYYY-MM-DDTHH:mm:ss.000Z`.|
| lang                              | Ko te reo o te tīhau e ai ki a Twitter. Ka kore te reo Māori i kitea i kōnei i te mea he kore mōhio o te API ki te reo Māori. |
| source                            | Ko te pūrere, te tautono o wāho rānei i tuku i te tīhau (arā 'Twitter Web Client', 'Twitter for iPhone'). |
| error								| Ko te take i kore tikiake ai i te tīhau. Ki te hē mai, kā whēnei: 'Authorization Error', 'Not Found Error', 'None'.| 

#### He rauemi i tua atu
- Ko te waehere i whakarite ai i tātari ai te putunga RMT kei kōnei [project GitHub repository](https://github.com/Waikato/kiwiwords/tree/master/rmt_corpus).
- E taea ana te <a href="../pics/rmt-v1-wordlist.csv">tikiake kupu rārangi</a> me te tatau o ngā kupu me ngā tohuhaki i te putunga nei.

#### Tohutoro te putunga RMT
Ki te whakamahi koe i te putunga RMT nei, tēnā koe me tohutoro whēnei mai:

- Trye, D., Keegan, T. T., Mato, P., & Apperley, M. (2022). [Harnessing Indigenous Tweets: The Reo Māori Twitter corpus](https://link.springer.com/article/10.1007/s10579-022-09580-w). <em>Lang Resources & Evaluation</em>, *56*, 1229-1268. doi:10.1007/s10579-022-09580-w

#### Kaimahi

- [David Trye](https://www.cs.waikato.ac.nz/~dgt12/)
- [Te Taka Keegan](https://www.cms.waikato.ac.nz/people/tetaka)
- [Paora Mato](https://www.waikato.ac.nz/php/research.php?mode=show&author=23169)
- [Mark Apperley](https://www.cms.waikato.ac.nz/people/mapperle)
- [Tamahau Brown](https://www.linkedin.com/in/tamahau-brown-9287b7139/)

Kaitautoko i tua:

- [Te Hiku Media](https://tehiku.nz/te-hiku-tech/), NZ
- [Kevin Scannell](https://cs.slu.edu/~scannell/index.html), Saint Louis University, US

#### Tautoko ā-pūtea
E mihi atu ana mō te tautoko ā-pūtea:

- Ngā Pae o te Māramatanga
- The University of Waikato

I whakatikahia te kōrero kei tēnei whārangi i Noema 2021. [Whakamōhio mai koa](mailto:dtrye@waikato.ac.nz) mehemea ka kite koe i ētehi hē i ngā waehere i tēneki whārangi rānei . I te Noema 2021, 72,575 tīhau (**91.85%** o te putunga RMT) i taea ai te tikiake i a Twitter.


### English
The *Reo Māori Twitter (RMT) Corpus* is a collection of 79,018 te reo Māori tweets, designed for linguistic analysis and to help in the development of new Natural Language Processing (NLP) resources for the Māori community. The corpus captures output from 2,302 users, including a mixture of personal and institutional accounts. These users were identified via Prof. Kevin Scannell's [Indigenous Tweets website](http://indigenoustweets.com/mi/).

#### Download the RMT Corpus
The tweets and user metadata in the RMT Corpus can be hydrated (downloaded from Twitter) using the code provided. The source code is adapted from Twitter's [sample code](https://github.com/twitterdev/Twitter-API-v2-sample-code) for API v2 endpoints.

Note: Some tweets in the corpus are no longer publicly available and, as such, cannot be downloaded. **Please [email David Trye](mailto:dtrye@waikato.ac.nz) if you would like access to the complete dataset, including additional metadata mentioned in our paper.**

The speed at which you can download the corpus depends on the [rate limit](https://developer.twitter.com/en/docs/twitter-api/rate-limits) for your Twitter developer account (e.g. 300 or 900 requests per 15-minute window). If you exceed the allocated limit, a 429 'Too many requests' error will be returned.

- Apply for a [Twitter developer account](https://developer.twitter.com/en/apply-for-access) if you do not have one already.
- Ensure that [Python 3](https://www.python.org/downloads/) is installed on your machine. The code for hydrating the corpus uses `requests==2.24.0`, which in turn uses `requests-oauthlib==1.3.0`. You can install these packages as follows:
```
pip install requests
pip install requests-oauthlib
```
- Download and extract all files in the <a href="../pics/rmt.zip">rmt</a> folder. This folder contains a file called `rmt-corpus-v1.csv`, which has the tweet IDs and selected metadata, as well as two Python scripts for downloading and formatting the data (namely, `get_tweets_with_bearer_token.py` and `json_to_tsv.py`).

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

#### Data Description: rmt-corpus-v1.csv

The following information (where known) is supplied in `rmt-corpus-v1.csv`, even if the tweet is no longer available on Twitter.

| Data Column                       | Description |
| -------------                     | ------------- |
| id                                | Twitter's unique identifier for the tweet. You can search for a tweet online by visiting [twitter.com/user/status/XXX](twitter.com/user/status/XXX), where `XXX` is the tweet's ID.  |
| num_maori_words                   | The number of Māori words in the tweet. |
| total_words                       | The total number of words in the tweet. |
| percent_maori                     | The percentage of Māori text detected in the tweet (=`num_maori_words` / `total_words`\*100). |
| favourites                        | The number of favourites (likes, retweets & quotes) that the given tweet received. |
| reply_count                       | The number of replies that the given tweet received. |
| user.alias                        | An alias for the author of the tweet in the form T`X`, where `X` represents the user’s ranking based on their total number of tweets in the corpus (`user.num_tweets`). |
| user.status                       | The account status (as of Decemeber 2020) of the user who wrote the tweet: 'active', 'protected', 'suspended' or 'not found'.|
| user.followers                    | The user's number of followers (as of December 2020). |
| user.friends                      | The number of accounts that the user follows (as of December 2020). |
| user.num_tweets                   | The total number of tweets in the corpus that were written by this user. |
| user.region                       | The user's location, based on self-reported information. Where possible, the data has been aggregated into [New Zealand regions](https://en.wikipedia.org/wiki/Regions_of_New_Zealand) and names of foreign countries. |
| year								| The year the tweet was written (between 2007 and 2020). |

#### Data Description: rmt-corpus-final.csv

If the tweet is still publicly available on Twitter, the following variables will appear alongside those mentioned above. Missing values are indicated with 'None':

| Data Column                       | Description |
| -------------                     | ------------- |
| content								| The tweet content, with consistent formatting applied (special characters stripped, user mentions and links standardised). |
| content_with_emojis								| The tweet content with emojis included. |
| conversation_id                   | The ID for the conversation that the tweet is part of. |
| in_reply_to_user_id               | If the tweet is written in reply to another, this is the ID of the user who who wrote the original tweet. | 
| author_id                         | Twitter's unique identifier for the user who wrote the tweet. |
| created_at                        | The timestamp when the tweet was posted, in the format `YYYY-MM-DDTHH:mm:ss.000Z`. |
| lang                              | The two-letter code representing the language that the tweet was (erroneously) classified as (NOT Māori, as the API does not support te reo). |
| source                            | The device or third-party application from which the tweet was posted (e.g. 'Twitter Web Client', 'Twitter for iPhone'). |
| error								| The reason why the tweet could not be downloaded, if there was an error ('Authorization Error', 'Not Found Error', 'None'). | 

#### Other Resources
- Code for cleaning and analysing the RMT Corpus is available on the [project GitHub repository](https://github.com/Waikato/kiwiwords/tree/master/rmt_corpus).
- You can <a href="../pics/rmt-v1-wordlist.csv">download a wordlist</a> with frequencies for all words and hashtags in the corpus.

#### Citing the RMT Corpus
If you use the RMT corpus, please cite the following paper:

- Trye, D., Keegan, T. T., Mato, P., & Apperley, M. (2022). [Harnessing Indigenous Tweets: The Reo Māori Twitter corpus](https://link.springer.com/article/10.1007/s10579-022-09580-w). <em>Lang Resources & Evaluation</em>, *56*, 1229-1268. doi:10.1007/s10579-022-09580-w

#### Team

- [David Trye](https://www.cs.waikato.ac.nz/~dgt12/)
- [Te Taka Keegan](https://www.cms.waikato.ac.nz/people/tetaka)
- [Paora Mato](https://www.waikato.ac.nz/php/research.php?mode=show&author=23169)
- [Mark Apperley](https://www.cms.waikato.ac.nz/people/mapperle)
- [Tamahau Brown](https://www.linkedin.com/in/tamahau-brown-9287b7139/)

External Collaborators:

- [Te Hiku Media](https://tehiku.nz/te-hiku-tech/), NZ
- [Kevin Scannell](https://cs.slu.edu/~scannell/index.html), Saint Louis University, US

#### Funding

We graciously acknowledge the generous support of:

- Ngā Pae o te Māramatanga
- The University of Waikato

The information on this page was last checked in November 2021. Please [let us know](mailto:dtrye@waikato.ac.nz) if you notice any errors in the code and/or instructions. 
As of 12 April 2021, 72,575 tweets (**91.85%** of the RMT Corpus) could be successfully downloaded from Twitter.
