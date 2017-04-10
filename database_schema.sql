-- host="***REMOVED***",    # your host, usually localhost
--                      user="***REMOVED***",        
--                      passwd="***REMOVED***",
--                      db="socialnetworkingdb"

-- To connect type in terminal: mysql -h ***REMOVED*** -P 3306 -u ***REMOVED*** -p socialnetworkingdb

SET FOREIGN_KEY_CHECKS = 0;

-- These commands will DELETE ANYTHING IN THE DB. BE CAREFUL.
DROP TABLE IF EXISTS TWEET;
DROP TABLE IF EXISTS USER;
DROP TABLE IF EXISTS HASHTAG;
DROP TABLE IF EXISTS TWEETSENTIMENT;
DROP TABLE IF EXISTS TWEETPOLITICAL;

CREATE TABLE TWEET (
    ID VARCHAR(100) PRIMARY KEY,
    tweet_text VARCHAR(500) NOT NULL DEFAULT '',
    user_id VARCHAR(100) NOT NULL DEFAULT 0,
    created_at DATETIME,
    retweet_count INT NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES USER(ID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE USER (
    ID VARCHAR(100) PRIMARY KEY,
    followers_count INT NOT NULL DEFAULT 0,
    friends_count INT NOT NULL DEFAULT 0,
    statuses_count INT NOT NULL DEFAULT 0,
    screen_name VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    verified BOOLEAN NOT NULL DEFAULT FALSE,
    location VARCHAR(250)
);

CREATE TABLE HASHTAG (
	tweet_id VARCHAR(100) NOT NULL,
	hashtag VARCHAR(150) NOT NULL,
	FOREIGN KEY (tweet_id) REFERENCES TWEET(ID) ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY (tweet_id, hashtag)
);

CREATE TABLE TWEETSENTIMENT (
	tweet_id VARCHAR(100) PRIMARY KEY,
	polarity DECIMAL NOT NULL,
	classification VARCHAR(100) NOT NULL,
	FOREIGN KEY (tweet_id) REFERENCES TWEET(ID) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Zakk fill in a create table statement for political table here.
-- Started it for you.

CREATE TABLE TWEETPOLITICAL (
    tweet_id VARCHAR(100) PRIMARY KEY,

    -- .... Stuff here..... --

    FOREIGN KEY (tweet_id) REFERENCES TWEET(ID) ON UPDATE CASCADE ON DELETE CASCADE
);

SET FOREIGN_KEY_CHECKS = 1;
