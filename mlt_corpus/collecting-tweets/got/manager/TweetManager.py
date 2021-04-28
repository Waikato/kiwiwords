
#encoding: utf-8

import urllib,urllib2,json,re,datetime,sys,cookielib
from .. import models
from pyquery import PyQuery

class TweetManager:
    
    def __init__(self):
        pass  
    
    @staticmethod
    def getTweets(tweetCriteria, receiveBuffer=None, bufferLength=100, proxy=None):
        refreshCursor = ''
        results = []
        resultsAux = []
        cookieJar = cookielib.CookieJar()
        
        if hasattr(tweetCriteria, 'username') and (tweetCriteria.username.startswith("\'") or tweetCriteria.username.startswith("\"")) and (tweetCriteria.username.endswith("\'") or tweetCriteria.username.endswith("\"")):
            tweetCriteria.username = tweetCriteria.username[1:-1]

        active = True

        while active:
            json = TweetManager.getJsonReponse(tweetCriteria, refreshCursor, cookieJar, proxy)
            if len(json['items_html'].strip()) == 0:
                break

            refreshCursor = json['min_position']
            scrapedTweets = PyQuery(json['items_html'])
            #Remove incomplete tweets withheld by Twitter Guidelines
            scrapedTweets.remove('div.withheld-tweet')
            tweets = scrapedTweets('div.js-stream-tweet')
            
            if len(tweets) == 0:
                break
            
            for tweetHTML in tweets:
                tweetPQ = PyQuery(tweetHTML)
                tweet = models.Tweet()
                
                usernameTweet = tweetPQ("span:first.username.u-dir b").text()
                #I added the underscore
                txt = re.sub(r"\s+", " ", tweetPQ("p.js-tweet-text").text().replace('# ', '#').replace('@ ', '@').replace('_ ', '_'))
                retweets = int(tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))
                favorites = int(tweetPQ("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))
                dateSec = int(tweetPQ("small.time span.js-short-timestamp").attr("data-time"))
                id = tweetPQ.attr("data-tweet-id")
                permalink = tweetPQ.attr("data-permalink-path")
                
                geo = ''
                geoSpan = tweetPQ('span.Tweet-geo')
                if len(geoSpan) > 0:
                    geo = geoSpan.attr('title')
                
                tweet.id = id
                tweet.permalink = 'https://twitter.com' + permalink
                tweet.username = usernameTweet
                tweet.text = txt
                tweet.date = datetime.datetime.fromtimestamp(dateSec)
                tweet.retweets = retweets
                tweet.favorites = favorites
                tweet.mentions = " ".join(re.compile('(@\\w*)').findall(tweet.text))
                tweet.hashtags = " ".join(re.compile('(#\\w*)').findall(tweet.text))
                tweet.geo = geo
                
                #Only include Tweets whose text contains the loanword (not just the username)
                #if (unidecode.unidecode(tweetCriteria.querySearch.lower()) in unidecode.unidecode(tweet.text.lower()) and "http" not in tweet.text):
                
                #print(tweet.username)
                
                #macrons = ["ā","ē","ī","ō","ū","Ā","Ē","Ī","Ō","Ū"]
                HAS_MACRON = False
                #print(tweet.mentions.lower())
                #FOR WORDS WITH MACRONS, BOTH VERSIONS NEED TO BE RUN.. 

                if HAS_MACRON:
                    results.append(tweet)
                    resultsAux.append(tweet)
                    #Need to filter out non-macron results, using macrons.py!

                if not HAS_MACRON:
                    if(tweetCriteria.querySearch.lower() in tweet.text.lower() and "http" not in tweet.text and "porn" not in tweet.text and tweetCriteria.querySearch.lower() not in tweet.mentions.lower()):
                        results.append(tweet)
                        resultsAux.append(tweet)
                
                if receiveBuffer and len(resultsAux) >= bufferLength:
                    receiveBuffer(resultsAux)
                    resultsAux = []
                
                if tweetCriteria.maxTweets > 0 and len(results) >= tweetCriteria.maxTweets:
                    active = False
                    break
                    
        
        if receiveBuffer and len(resultsAux) > 0:
            receiveBuffer(resultsAux)
        
        return results
    
    @staticmethod
    def getJsonReponse(tweetCriteria, refreshCursor, cookieJar, proxy):
        url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&max_position=%s"

        #Remove tweets containing URLs
        urlGetData = '-filter:links'
        
        if hasattr(tweetCriteria, 'username'):
            urlGetData += ' from:' + tweetCriteria.username
        
        if hasattr(tweetCriteria, 'querySearch'):
            urlGetData += ' ' + tweetCriteria.querySearch
        
        if hasattr(tweetCriteria, 'near'):
            urlGetData += "&near:" + tweetCriteria.near + " within:" + tweetCriteria.within
        
        if hasattr(tweetCriteria, 'since'):
            urlGetData += ' since:' + tweetCriteria.since
            
        if hasattr(tweetCriteria, 'until'):
            urlGetData += ' until:' + tweetCriteria.until

        if hasattr(tweetCriteria, 'topTweets'):
            if tweetCriteria.topTweets:
                url = "https://twitter.com/i/search/timeline?q=%s&src=typd&max_position=%s"
        
        urlGetData += ' lang:en'
        url = (url % (urllib.quote(urlGetData), urllib.quote(refreshCursor)))

        headers = [
            ('Host', "twitter.com"),
            ('User-Agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"),
            ('Accept', "application/json, text/javascript, */*; q=0.01"),
            ('Accept-Language', "de,en-US;q=0.7,en;q=0.3"),
            ('X-Requested-With', "XMLHttpRequest"),
            ('Referer', url),
            ('Connection', "keep-alive")
        ]

        if proxy:
            opener = urllib2.build_opener(urllib2.ProxyHandler({'http': proxy, 'https': proxy}), urllib2.HTTPCookieProcessor(cookieJar))
        else:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
        opener.addheaders = headers

        try:
            response = opener.open(url)
            jsonResponse = response.read()
            #print "https://twitter.com/search?q=%s&src=typd" % urllib.quote(urlGetData)
        except:            
            print "Error, check URL in browser: https://twitter.com/search?q=%s&src=typd" % urllib.quote(urlGetData)
            sys.exit()
            return
    
        dataJson = json.loads(jsonResponse)
        
        return dataJson        
