### This script is to pre-process data downloaded from Richard's couch DB ######

1 Download data through curl command on the server:
- cd to process_data directory
- run: curl -XGET "http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/summary?include_docs=true&reduce=f
alse&start_key=\[\"r1r0\",2014,1,1\]&skip=0&limit=300000" --user "readonly:ween7ighai9gahR6" >> dataoutput1.json

- Run this command on three servers and generate dataoutpu1.json, dataoutpu2.json and dataoutpu3.json respectively, which is to be processed by our script

2 How to invoke the script?
You can run 'python process_data.py 1'. 
It means this script will be run with the first group of configuration. You can also change this parametter to 2 or 3.

3 what is the output?
All tweets in Melbourne will be appended 'sentiment' attribute. All tweets within the range will be appended with 'SA2 code' attribute. 
