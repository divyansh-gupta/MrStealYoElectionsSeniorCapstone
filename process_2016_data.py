import sys
import tweepy
import os
import pickle


auth = tweepy.OAuthHandler("***REMOVED***", 
                            "***REMOVED***")

auth.set_access_token(
    "***REMOVED***",
    "***REMOVED***")

api = tweepy.API(auth)

# print api.rate_limit_status()
# for file in os.listdir("2016_used"):
    # current_file = open("2016_used/"+file, "r")
# file = open("2016_used/election-filter1.txtcc", "r")
# print "opened file"



# current_line = 0
# for i in range(len(all_lines)):
#     current_ids = []
#     for n in range(100):
#         temp = all_lines.pop(i)
#         current_ids.append(temp.strip("\n"))
#         current_line += 1

#     print "Size of all_lines: ", len(all_lines)
#     print "Current ids: ", current_ids
#     statuses = api.statuses_lookup(current_ids)
#     print "========================================================"
#     print current_line
#     print statuses[0]._json['text'].encode("utf-8")
#     if current_line == 100:
#         break;


pclassifier = None
def main():
    if os.path.exists('2016_data') is False:
        os.makedirs('2016_data')

    classifier_file_name = 'c1.classifier'
    if os.path.exists(classifier_file_name) is False:
        print('downloading classifier file from s3')
        s3.download_from_s3('social-networking-capstone', classifier_file_name, classifier_file_name, True)
    classifier_file = open(classifier_file_name, 'rb')
    global pclassifier
    pclassifier = pickle.load(classifier_file)
    classifier_file.close()
    print('classifier loaded')

    files_to_process = os.listdir("2016_data")
    tweet_processor = TwitterClient(pclassifier)

    for file in files_to_process:
        lines_in_file = []
        ids_to_process = []
        for line in file:
            lines_in_file.append(line)
        for i in range(len(all_lines)):
            ids_to_process = []
            for n in range(100):
                temp = lines_in_file.pop(i)
                ids_to_process.append(temp.strip("\n"))
                current_line += 1

            # print "Size of all_lines: ", len(lines_in_file)
            # print "Current ids: ", current_ids
            statuses = api.statuses_lookup(current_ids)
            statuses_json = []
            for x in range(len(statuses)):
                statuses_json.append(statuses[i]._json)
            tweet_processor.process_tweet(statuses_json)



if __name__ == "__main__":
    main()