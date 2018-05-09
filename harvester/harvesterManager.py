from searchAPIHarvester import TweetProcessor
from configs import configs
from streamAPIHarvester import TweetStreamProcessor


import couchdb
import sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('harvester-manager.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

if __name__ == '__main__':
    try:
        # The user is expected to tell which processor should be run
        harvester_id = int(sys.argv[1])
        # If user inputs a valid since_id, pass it to searchAPIHarvester
        try:
            since_id = int(sys.argv[2])
        except Exception:
            since_id = None

        # Fetch the corresponding processor's configuration information
        conf = configs[harvester_id]
        couchserver = couchdb.Server('http://'+conf['couchdb-admin-username']+':'
                                     +conf['couchdb-admin-password'] + '@'
                                     +conf['couchdb-address'])
        db = couchserver[conf['couchdb-db-name']]

        logger.info('Database connection established')

        thread_tweetPrc = TweetProcessor(conf['consumer_key'], conf['consumer_secret'],conf['access_token'],
                                         conf['access_token_secret'], conf['twitter-geo-latlngrad'],str(harvester_id), db, since_id)
        thread_tweetstreamPrc = TweetStreamProcessor(conf['consumer_key'], conf['consumer_secret'],
                                  conf['access_token'], conf['access_token_secret'], conf['twitter-geo-rec'],str(harvester_id), db)

        logger.info('TweetProcessor created')
        logger.info('TweetStreamProcessor created')
        # Running two threads at the same time
        thread_tweetstreamPrc.start()
        thread_tweetPrc.start()

    except IndexError:
        print('Processor Number should be given')
    except Exception as e:
        logger.error(str(e))
