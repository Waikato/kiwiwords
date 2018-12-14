
echo "CL: NaiveBayes	AT: Unigrams"

java -Xmx4G -cp /home/fbravoma/weka-3-8-2/weka.jar weka.Run weka.classifiers.meta.FilteredClassifier -t /home/fbravoma/loanwords/tweets.test.target.arff -classifications "weka.classifiers.evaluation.output.prediction.CSV -use-tab -p first-last -file naiveBayesPred.csv" -o -v -F "weka.filters.MultiFilter -F \"weka.filters.unsupervised.attribute.TweetToSparseFeatureVector -E 5 -D 3 -I 0 -F -M 3 -G 0 -taggerFile /home/fbravoma/wekafiles/packages/AffectiveTweets/resources/model.20120919 -wordClustFile /home/fbravoma/wekafiles/packages/AffectiveTweets/resources/50mpaths2.txt.gz -Q 1 -red -stan -stemmer weka.core.stemmers.NullStemmer -stopwords-handler \\\"weka.core.stopwords.Null \\\" -I 2 -U -tokenizer \\\"weka.core.tokenizers.TweetNLPTokenizer \\\"\" -F \"weka.filters.unsupervised.attribute.Reorder -R 4-last,3\"" -S 1 -W weka.classifiers.bayes.NaiveBayesMultinomial



weka.filters.unsupervised.attribute.TweetToSparseFeatureVector -E 5 -D 3 -I 0 -F -M 3 -G 0 -taggerFile /home/fbravoma/wekafiles/packages/AffectiveTweets/resources/model.20120919 -wordClustFile /home/fbravoma/wekafiles/packages/AffectiveTweets/resources/50mpaths2.txt.gz -Q 1 -red -stan -stemmer weka.core.stemmers.NullStemmer -stopwords-handler "weka.core.stopwords.Null " -I 2 -U -tokenizer "weka.core.tokenizers.TweetNLPTokenizer "

weka.filters.unsupervised.attribute.Reorder -R 4-last,3



weka.filters.MultiFilter -F "weka.filters.unsupervised.attribute.TweetToSparseFeatureVector -E 5 -D 3 -I 0 -F -M 3 -G 0 -taggerFile /home/fbravoma/wekafiles/packages/AffectiveTweets/resources/model.20120919 -wordClustFile /home/fbravoma/wekafiles/packages/AffectiveTweets/resources/50mpaths2.txt.gz -Q 1 -red -stan -stemmer weka.core.stemmers.NullStemmer -stopwords-handler \"weka.core.stopwords.Null \" -I 2 -U -tokenizer \"weka.core.tokenizers.TweetNLPTokenizer \"" -F "weka.filters.unsupervised.attribute.Reorder -R 4-last,3"


Unigrams + NaiveBayes
weka.classifiers.meta.FilteredClassifier -F "weka.filters.MultiFilter -F \"weka.filters.unsupervised.attribute.TweetToSparseFeatureVector -E 5 -D 3 -I 0 -F -M 3 -G 0 -taggerFile /home/fbravoma/wekafiles/packages/AffectiveTweets/resources/model.20120919 -wordClustFile /home/fbravoma/wekafiles/packages/AffectiveTweets/resources/50mpaths2.txt.gz -Q 1 -red -stan -stemmer weka.core.stemmers.NullStemmer -stopwords-handler \\\"weka.core.stopwords.Null \\\" -I 2 -U -tokenizer \\\"weka.core.tokenizers.TweetNLPTokenizer \\\"\" -F \"weka.filters.unsupervised.attribute.Reorder -R 4-last,3\"" -S 1 -W weka.classifiers.bayes.NaiveBayesMultinomial
