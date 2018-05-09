import tweepy
from textblob import TextBlob
import logging
import json
import threading
from check_location_handler import Check_Location_Handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('stream-api.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class MyStreamListener(tweepy.StreamListener):

    def __init__(self, processor_id, couchdb, api):
        super(tweepy.StreamListener, self).__init__()
        self.processor_id = processor_id
        self.couchdb = couchdb
        self.api = api


    def on_data(self, data):
        try:

            tweet = json.loads(data)

            sentiment = TextBlob(tweet['text']).sentiment.polarity

            if tweet and tweet['coordinates'] and tweet['coordinates']['coordinates']:

                # This is a way to get the 100 recent tweets of the people who have included their geolocation in
                # their tweets and stores them as well
                resp = self.api.user_timeline(user_id=tweet['user']['id'], count=100)
                for status in resp:

                    status_json = status._json

                    lat = status_json['coordinates']['coordinates'][1]
                    log = status_json['coordinates']['coordinates'][0]

                    response_properties = Check_Location_Handler.append_attribute(log, lat)

                    if response_properties is not None:
                        response_properties['sentiment'] = sentiment
                        process_info = {'properties': response_properties,'sentiment': sentiment, 'processor-id': self.processor_id}
                        logger.info('With location:' + (str(status_json['id'])))
                    # For those coordinates not in the json grid
                    else:
                        process_info = {'sentiment': sentiment, 'processor-id': self.processor_id}
                    status_json['process-info'] = process_info
                    self.couchdb[str(status_json['id'])] = status_json

            # For those without coordinate information, we only append sentiment analysis and processor id
            else:
                process_info = {'sentiment': sentiment, 'processor-id': self.processor_id}
                tweet['process-info'] = process_info

                self.couchdb[str(tweet['id'])] = tweet

            logger.info('StreamAPI tweet added to the database with id: ' + str(tweet['id']))

        except Exception as e:
            logger.info(str(e) + ' Skipped stream twitter id:' + str(tweet['id']))


    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False


class TweetStreamProcessor(threading.Thread):

    def __init__(self, twitter_consumer_key, twitter_consumer_secret, twitter_access_token,
                 twitter_access_token_secret, twitter_geo_param_rec, processor_id, couchdb):
        threading.Thread.__init__(self)
        self.twitter_consumer_key = twitter_consumer_key
        self.twitter_consumer_secret = twitter_consumer_secret
        self.twitter_access_token = twitter_access_token
        self.twitter_access_secret = twitter_access_token_secret
        self.twitter_geo_param_rec = twitter_geo_param_rec
        self.processor_id = processor_id
        self.couchdb = couchdb

        auth = tweepy.OAuthHandler(self.twitter_consumer_key, self.twitter_consumer_secret)
        auth.set_access_token(self.twitter_access_token, self.twitter_access_secret)

        self.api = tweepy.API(auth, wait_on_rate_limit=True,
                   wait_on_rate_limit_notify=True)

    def run(self):
        try:
            myStreamListener = MyStreamListener(self.processor_id, self.couchdb, self.api)
            myStream = tweepy.Stream(auth=self.api.auth, listener=myStreamListener)
            # Process tweets from the filter.json API endpoint, and passing them to listener
            myStream.filter(locations=self.twitter_geo_param_rec)
        except Exception as e:
            logger.error(str(e))

