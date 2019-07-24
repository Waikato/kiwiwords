# -*- coding: utf-8 -*-
import sys,getopt,codecs
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got
from os.path import isfile

def main(argv):

    if len(argv) == 0:
        print('You must pass some parameters. Use \"-h\" to help.')
        return

    if len(argv) == 1 and argv[0] == '-h':
        f = open('exporter_help_text.txt', 'r')
        print f.read()
        f.close()

        return

    try:
        opts, args = getopt.getopt(argv, "", ("username=", "near=", "within=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "output="))

        tweetCriteria = got.manager.TweetCriteria()        

        for opt,arg in opts:
            if opt == '--username':
                tweetCriteria.username = arg

            elif opt == '--since':
                tweetCriteria.since = arg

            elif opt == '--until':
                tweetCriteria.until = arg

            elif opt == '--querysearch':
                tweetCriteria.querySearch = arg

            elif opt == '--toptweets':
                tweetCriteria.topTweets = True

            elif opt == '--maxtweets':
                tweetCriteria.maxTweets = int(arg)
            
            elif opt == '--near':
                tweetCriteria.near = '"' + arg + '"'
            
            elif opt == '--within':
                tweetCriteria.within = '"' + arg + '"'

            elif opt == '--within':
                tweetCriteria.within = '"' + arg + '"'

            elif opt == '--output':
                outputFilename = arg
        
        outputFilename = "%s.csv" % tweetCriteria.querySearch
        #while isfile(outputFilename % sequence):
        #    sequence = int(sequence or 0) + 1
        #outputFilename = outputFilename % sequence        
        outputFile = codecs.open(outputFilename, "w+", "utf-8")

        outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')

        print('Searching...\n')

        def receiveBuffer(tweets):
            for t in tweets:
                outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink)))
            outputFile.flush()
            print('Another %d Tweets saved to file...\n' % len(tweets))

        got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

    except arg:
        print('Arguments parser error, try -h' + arg)
    finally:
        outputFile.close()
        print('Done! Saved to "%s".' % outputFilename)

if __name__ == '__main__':
    main(sys.argv[1:])
