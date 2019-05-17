# The Corpus
<br>
The Māori Loanword Twitter Corpus (<i>MLT Corpus</i>) is a diachronic corpus of tweets from 2008-2018 that were harvested using 77 "query words" (Māori words of interest). It consists of three key components:

1. <i>Raw Corpus</i>: 1.6 million Tweets containing at least one query word, some of which are <i>not</i> used in relevant (NZE) contexts.
2. <i>Labelled Corpus</i>: 3,685 Tweets that were manually labelled as relevant (i.e. the query words they contain <i>are</i> used in relevant contexts).
3. <i>Processed Corpus</i>: 1.1 million Tweets that were <i>classified</i> as relevant by a machine learning model which used the <i>Labelled Corpus</i> as training data. 

Below is a description of these components and a flowchart outlining how the <i>Processed Corpus</i> was built. 

### Key Stats
| Description          | Raw Corpus | Labelled Corpus | Processed Corpus |
| ---------------------|------------|-----------------| -----------------|
| Tokens (words)       | 28,804,640 | 49,477          | 21,810,637       |
| Tweets               | 1,628,042  | 2,495           | 1,179,390        |
| Tweeters (authors)   | 604,006    | 1,866           | 426,280          |

### Building the Corpus
 <img src="../pics/Process2.png" alt="Process" width="1500"/>
