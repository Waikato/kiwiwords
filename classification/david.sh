echo "CL: NaiveBayes FS: Unigrams"


java -Xmx4G -cp /home/fbravoma/weka-3-8-2/weka.jar weka.Run weka.classifiers.meta.FilteredClassifier -t tweets.test.target.arff -v -o -d naiveBayes-unigrams.model -classifications "weka.classifiers.evaluation.output.prediction.CSV -use-tab -p first-last -file naiveBayes-Unigrams-Pred.csv" -F "weka.filters.MultiFilter -F \"weka.filters.unsupervised.attribute.TweetToSparseFeatureVector -E 5 -D 3 -I 0 -F -M 3 -G 0 -taggerFile /home/fbravoma/wekafiles/packages/AffectiveTweets/resources/model.20120919 -wordClustFile /home/fbravoma/wekafiles/packages/AffectiveTweets/resources/50mpaths2.txt.gz -Q 1 -red -stan -stemmer weka.core.stemmers.NullStemmer -stopwords-handler \\\"weka.core.stopwords.Null \\\" -I 2 -U -tokenizer \\\"weka.core.tokenizers.TweetNLPTokenizer \\\"\" -F \"weka.filters.unsupervised.attribute.Reorder -R 4-last,3\"" -S 1 -W weka.classifiers.functions.LibLINEAR -- -S 7 -C 1.0 -E 0.001 -B 1.0 -P -L 0.1 -I 1000




java -Xmx4G -cp /home/fbravoma/weka-3-8-2/weka.jar weka.Run weka.classifiers.meta.FilteredClassifier -l /home/fbravoma/loanwords/naiveBayes-unigrams.model -T tweets.test.unk.arff -classifications "weka.classifiers.evaluation.output.prediction.CSV -use-tab -p first-last -file naiveBayes-Unigrams-Pred-Target.csv"





java -Xmx4G -cp /home/fbravoma/weka-3-8-2/weka.jar weka.Run weka.classifiers.misc.SerializedClassifier -model /home/fbravoma/loanwords/naiveBayes-unigrams.model -T tweets.test.target.target.arff -v -o -d naiveBayes-unigrams.model -classifications "weka.classifiers.evaluation.output.prediction.CSV -use-tab -p first-last -file naiveBayes-Unigrams-Pred-Target.csv"
