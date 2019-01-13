weka.filters.unsupervised.attribute.TweetToSparseFeatureVector -A -E 5 -D 2 -I 0 -F -M 4 -G 0 -taggerFile /home/fbravoma/wekafiles/packages/AffectiveTweets/resources/model.20120919 -wordClustFile /home/fbravoma/wekafiles/packages/AffectiveTweets/resources/50mpaths2.txt.gz -Q 0 -stemmer weka.core.stemmers.NullStemmer -stopwords-handler "weka.core.stopwords.Null " -I 1 -U -tokenizer "weka.core.tokenizers.TweetNLPTokenizer "

weka.filters.unsupervised.attribute.Reorder -R 3-last,2


weka.filters.MultiFilter -F "weka.filters.unsupervised.attribute.TweetToSparseFeatureVector -A -E 5 -D 2 -I 0 -F -M 4 -G 0 -taggerFile /home/fbravoma/wekafiles/packages/AffectiveTweets/resources/model.20120919 -wordClustFile /home/fbravoma/wekafiles/packages/AffectiveTweets/resources/50mpaths2.txt.gz -Q 0 -stemmer weka.core.stemmers.NullStemmer -stopwords-handler \"weka.core.stopwords.Null \" -I 1 -U -tokenizer \"weka.core.tokenizers.TweetNLPTokenizer \"" -F "weka.filters.unsupervised.attribute.Reorder -R 3-last,2"


weka.classifiers.functions.LibLINEAR -S 7 -C 1.0 -E 0.001 -B 1.0 -P -L 0.1 -I 1000


weka.filters.supervised.instance.Resample -B 1.0 -S 1 -Z 20.0


weka.classifiers.meta.FilteredClassifier -F "weka.filters.MultiFilter -F \"weka.filters.unsupervised.attribute.TweetToSparseFeatureVector -A -E 5 -D 2 -I 0 -F -M 4 -G 0 -taggerFile /home/fbravoma/wekafiles/packages/AffectiveTweets/resources/model.20120919 -wordClustFile /home/fbravoma/wekafiles/packages/AffectiveTweets/resources/50mpaths2.txt.gz -Q 0 -stemmer weka.core.stemmers.NullStemmer -stopwords-handler \\\"weka.core.stopwords.Null \\\" -I 1 -U -tokenizer \\\"weka.core.tokenizers.TweetNLPTokenizer \\\"\" -F \"weka.filters.unsupervised.attribute.Reorder -R 3-last,2\"" -S 1 -W weka.classifiers.functions.LibLINEAR -- -S 7 -C 1.0 -E 0.001 -B 1.0 -P -L 0.1 -I 1000
