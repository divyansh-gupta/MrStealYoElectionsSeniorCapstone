import json
import sys
from pprint import pprint

first_arg = sys.argv[1]

with open(first_arg) as data_file:
    try:
        data = json.load(data_file)
        pprint(data['text'])
        json_str = json.dumps(data)
        with open(first_arg, 'w') as f:
            json.dump(data['text'], f) 
            #to make handling the file size eaiser rewrite the "text" within the orignal json file
    except IOError as e:
            pprint ("I/O error({0}): {1}".format(e.errno, e.strerror))
    except ValueError:
            pprint ("Could not convert data to an integer.")
    except:
            print ("Unexpected error:", sys.exc_info()[0])
            raise
