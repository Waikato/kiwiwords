import sys
from datetime import date
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

def main():

	def printTweet(t):
		#print(descr)
		#print("Username: %s" % t.username)
		#print("Retweets: %d" % t.retweets)
		print(t.text)
		#print("Mentions: %s" % t.mentions)
		#print("Hashtags: %s\n" % t.hashtags)

	# Example 2 - Get tweets by query search
	#tweetCriteria = got.manager.TweetCriteria().setQuerySearch('whetu').setSince("2006-03-21").setUntil("2018-10-20").setMaxTweets(5)
	#tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

	#printTweet(tweet)

if __name__ == '__main__':
	main()
