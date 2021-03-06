# streaming the tweets directly from twitter in realtime. 
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor

import twitter_credentials

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth=TwitterAuthenticator().authenticate_twitter()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user
        
    def get_user_tweets(self, num_tweets):
        tweets = []
        for t in Cursor(self.twitter_client.user_timeline, id= self.twitter_user).items(num_tweets):
            tweets.append(t)
        return tweets

#we want to create a clasa which will allow us to print the tweets. 
#we call it stdoutListener, and it is going to inherit from StreamListener
#stdoutListener has some methods that we want to override.
class TwitterAuthenticator():
    def  authenticate_twitter(self):
        auth = OAuthHandler(twitter_credentials.consumer_key, twitter_credentials.consumer_secret)
        auth.set_access_token(twitter_credentials.access_token, twitter_credentials.access_token_secret)   
        return auth

class TwitterStreamer():
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()##

    def stream_tweets(self, tweets_filename, hashtags_list):
        listener = MyListener(tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter()##
        stream = Stream(auth, listener)
        stream.filter(track=hashtags_list)


class MyListener(StreamListener):

    def __init__(self, tweets_filename):
        self.tweets_filename = tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          

    def on_error(self, status):
        if status ==420:
            return False
        print(status)

if __name__ == '__main__':
 
    hash_tag_list = ["#تسقط_بس", "#مدن_السودان_تنتفض", "#SudanUprise", "#SudanRevolts"]
    fetched_tweets_filename = "tweets.txt"

    twitter_client = TwitterClient('IBM')
    print(twitter_client.get_user_tweets(1))
   # twitter_streamer = TwitterStreamer()
   # twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
    