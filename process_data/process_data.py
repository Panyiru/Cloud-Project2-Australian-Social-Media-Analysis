import json
from textblob import TextBlob
from check_location_handler import Check_Location_Handler
import couchdb
import logging
import sys
from config import configs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('process_data.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# This script is to append 'process-info' to twitters downloaded from lecturer's url
if __name__ == '__main__':
    try:
        server_id = int(sys.argv[1])
        file_name = configs[server_id]['file_name']
        processor_id=configs[server_id]['processor_id']

        couchserver = couchdb.Server(configs[server_id]['couch_server'])
        db = couchserver[configs[server_id]['db_name']]

        with open(file_name, 'r') as raw_file:
            for line in raw_file:
                try:
                    raw_json = json.loads(line.strip()[:-1])
                    tweet = raw_json['doc']
                    del tweet['_id']
                    del tweet['_rev']

                    sentiment = TextBlob(tweet['text']).sentiment.polarity

                    if tweet and tweet['coordinates'] and tweet['coordinates']['coordinates']:
                        lat = tweet['coordinates']['coordinates'][1]
                        log = tweet['coordinates']['coordinates'][0]

                        response_properties = Check_Location_Handler.append_attribute(log, lat)

                        if response_properties is not None:
                            response_properties['sentiment'] = sentiment
                            process_info = {'properties': response_properties,
                                            'sentiment': sentiment, 'processor-id': processor_id}
                            print('With location:' + (str(tweet['id'])))
                        # For those coordinates not in the json grid
                        else:
                            process_info = {'sentiment': sentiment, 'processor-id': processor_id}

                    else:
                        process_info = {'sentiment': sentiment, 'processor-id': processor_id}

                    tweet['process-info'] = process_info

                    db[str(tweet['id'])] = tweet

                    print("Tweet added to the database with id: " + str(tweet['id']))

                except Exception as e:
                    print(str(e))

    except Exception as e:
        print(str(e))