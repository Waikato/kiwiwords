# The MLT Corpus
<br>
The Māori Loanword Twitter Corpus (<i>MLT Corpus</i>) is a diachronic corpus of nearly 3 million New Zealand English tweets, posted between 2008 and 2018. The data was collected by extracting tweets containing one or more terms from a list of 77 Māori words and phrases. We then used computational machine learning methods to clean up the raw data, because many of the tweets were not relevant to a New Zealand English context (for instance, the loanword <i>Moana</i>, meaning sea, is commonly used to refer to the Disney film/princess).

The corpus consists of three key components:

1. <i>Raw Corpus</i>: The original dataset, which includes many irrelevant (non-New Zealand English) tweets.
2. <i>Labelled Corpus</i>: 3,685 tweets that were manually labelled as "relevant" or "irrelevant" and used as training data for our model.
3. <i>Processed Corpus</i>: The final version of the corpus, containing only tweets that the model classified as relevant.

### Building the MLT Corpus
Below is a visual representation of the steps involved in building the corpus.
<img src="../pics/Process2.png" alt="Process" width="1500"/>

For further information, see [our paper](https://www.aclweb.org/anthology/P19-2018/). 

### Summary Statistics
This table shows key stats for the different components of the MLT Corpus:

| Description          |Raw Corpus V2*| Labelled Corpus | Processed Corpus V2*|
| ---------------------|--------------|-----------------|---------------------| 
| Tokens (words)       | 70,964,941   |49,477           | 46,827,631          | 
| Tweets               | 4,559,105    | 2,495           | 2,880,211           |
| Tweeters (authors)   | 1,839,707    | 1,866           | 1,226,109           |

\*Please note that these statistics differ from what is stated in the paper, because we later refined our classifier, opting for a Naive Bayes Multinomial model that considered both unigrams and bigrams. 

### Download the MLT Corpus
Click to <a href="../pics/mlt-v2.zip">download the MLT Corpus</a>.

### Citing the MLT Corpus
If you use the MLT corpus, please cite the following paper:
<br>
Trye, D., Calude, A., Bravo-Marquez, F., Keegan, T. T. (2019). [Māori loanwords: A corpus of New Zealand English tweets](https://www.aclweb.org/anthology/P19-2018/). In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics: Student Research Workshop, pp. 136–142. Florence, Italy: Association for Computational Linguistics. doi:10.18653/v1/P19-2018. 
