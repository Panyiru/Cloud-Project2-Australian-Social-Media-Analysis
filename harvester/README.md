### This is the script file for harvesters. ###
1 Where to install?
This harvester script should be run on three NeCTAR servers separately and parallelly.

2 How to invoke the application?
You can run it using “nohup python harvesterManager.py 2”. 
‘nohup’ means this script will continue to run at backend even if you close your terminator. The first parameter ‘2’ indicates that this is the harvester No.2. Thus, this harvester will utilize the second group of information in config files, including different twitter API 
authentication keys and different searching ranges.

You can also run it using “nohup python harvesterManager.py 2 990000000000000000”. The second parameter is the since_id for Search API. 
Harvesters will not search tweets whose ids are smaller than this since_id. It’s useful when you collect data for the second round and 
you probably don’t want to search for the tweets earlier than the latest tweet from last round.
