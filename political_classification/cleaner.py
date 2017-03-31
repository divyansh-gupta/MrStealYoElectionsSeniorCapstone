import json
import sys
from pprint import pprint
from ../constants.py import Classifications

#get tweets for account X
#practice tweets
tweet_list = [{"text": "this is a democratic tweet"}, {"text": "this is another democratic tweet"}]

label = Classifications.democrat

fname = 'labelled.json'

f = open(fname, 'a')

for tweet in tweet_list:
	data = {}
	data['text'] = tweet['text']
	data['label'] = label
	try:
		json.dump(data, f)
	except IOError as e:
            pprint ("I/O error({0}): {1}".format(e.errno, e.strerror))
    except ValueError:
            pprint ("Could not convert data to an integer.")
    except:
            print ("Unexpected error:", sys.exc_info()[0])
            raise
	

# with open(first_arg) as data_file:
    # try:
        # data = json.load(data_file)
        # pprint(data['text'])
        # json_str = json.dumps(data)
        # with open(first_arg, 'w') as f:
			# jsonobj
            # json.dump(data['text'], f) 
            # #to make handling the file size eaiser rewrite the "text" within the orignal json file
    # except IOError as e:
            # pprint ("I/O error({0}): {1}".format(e.errno, e.strerror))
    # except ValueError:
            # pprint ("Could not convert data to an integer.")
    # except:
            # print ("Unexpected error:", sys.exc_info()[0])
            # raise
