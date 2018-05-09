import tweepy
from textblob import TextBlob
import logging
import threading
from check_location_handler import Check_Location_Handler


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('search-api.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

"""
Skeleton taken from https://dev.to/bhaskar_vk/how-to-use-twitters-search-rest-api-most-effectively
"""


class TweetProcessor(threading.Thread):
    def __init__(self,twitter_consumer_key, twitter_consumer_secret, twitter_access_token,
                 twitter_access_token_secret, twitter_geo_param, processor_id, couchdb, since_id=None, max_id=-1,tweets_per_query=100,
                 search_query='*'):
        threading.Thread.__init__(self)
        self.twitter_consumer_key = twitter_consumer_key
        self.twitter_consumer_secret = twitter_consumer_secret
        self.twitter_access_token = twitter_access_token
        self.twitter_access_token_secret = twitter_access_token_secret
        self.twitter_geo_param = twitter_geo_param
        self.couchdb = couchdb
        self.since_id = since_id
        self.max_id = max_id
        self.tweets_per_query = tweets_per_query
        self.search_query = search_query
        self.processor_id = processor_id

        auth = tweepy.OAuthHandler(self.twitter_consumer_key, self.twitter_consumer_secret)

        self.api = tweepy.API(auth, wait_on_rate_limit=True,
                        wait_on_rate_limit_notify=True)

        if not self.api:
            print("Can't Authenticate")


    def run(self):


        # If results from a specific ID onwards are read, set since_id to that ID.
        # else default to no lower limit, go as far back as API allows

        # If results only below a specific ID are, set max_id to that ID.
        # else default to no upper limit, start from the most recent tweet matching the search query.

        maxTweets = 100000000  # Some arbitrary large number
        tweetCount = 0
        while tweetCount < maxTweets:
            try:
                if self.max_id <= 0:
                    if not self.since_id:
                        new_tweets = self.api.search(q=self.search_query, count=self.tweets_per_query,geocode=self.twitter_geo_param)
                    else:
                        new_tweets = self.api.search(q=self.search_query, count=self.tweets_per_query,
                                                since_id=self.since_id,geocode=self.twitter_geo_param)
                else:
                    if not self.since_id:
                        new_tweets = self.api.search(q=self.search_query, count=self.tweets_per_query,
                                                max_id=str(self.max_id - 1),geocode=self.twitter_geo_param)
                    else:
                        new_tweets = self.api.search(q=self.search_query, count=self.tweets_per_query,
                                                max_id=str(self.max_id - 1),
                                                since_id=self.since_id, geocode=self.twitter_geo_param)
                if not new_tweets:
                    logger.error("No more tweets found. Quitting...")
                    break

                tweetCount += len(new_tweets)

                for twit_obj in new_tweets:
                    try:
                        tweet = twit_obj._json
                        sentiment = TextBlob(tweet['text']).sentiment.polarity

                        if tweet and tweet['coordinates'] and tweet['coordinates']['coordinates']:
                            lat = tweet['coordinates']['coordinates'][1]
                            log = tweet['coordinates']['coordinates'][0]

                            response_properties = Check_Location_Handler.append_attribute(log,lat)

                            if response_properties is not None:
                                response_properties['sentiment'] = sentiment
                                process_info = {'properties':response_properties,
                                            'sentiment': sentiment, 'processor-id': self.processor_id}
                                logger.info('With location:'+(str(tweet['id'])))
                            # For those coordinates not in the json grid
                            else:
                                process_info = {'sentiment': sentiment, 'processor-id': self.processor_id}

                        else:
                            process_info = {'sentiment': sentiment, 'processor-id': self.processor_id}

                        tweet['process-info'] = process_info

                        self.couchdb[str(tweet['id'])] = tweet

                        logger.info("SearchAPI tweet added to the database with id: " + str(tweet['id']))

                    except Exception as e:
                        logger.info(str(e) + " Skipped search twitter id:" + str(tweet['id']))


                logger.info("Downloaded {0} tweets".format(tweetCount))
                self.max_id = new_tweets[-1].id

            except tweepy.TweepError as e:
                # Just exit if any error
                logger.exception("Tweepy error : " + str(e))
                break
