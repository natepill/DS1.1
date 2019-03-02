from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import requests
import tweepy
import env #Custom env file for tweepy keys
import dataset
import json
import os




db = dataset.connect("sqlite:///tweets.db")
table = db["tweets"]



auth = tweepy.OAuthHandler(env.TWITTER_APP_KEY, env.TWITTER_APP_SECRET)
auth.set_access_token(env.TWITTER_APP_KEY, env.TWITTER_APP_SECRET)



# Twitter sent, and call an appropriate method to deal with the specific data type. It's possible to deal with events like users sending direct messages, tweets being deleted, and more. For now, we only care about when users post tweets. Thus, we'll need to override the on_status method:

#Overriding Tweepy's StreamListener class
class StreamListener(tweepy.StreamListener):
    '''Create a listener that prints the text of any tweet that comes from the Twitter API.'''

    def on_status(self, status):
        if status.retweeted_status:
            return
        print(status.text)

        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color

        blob = TextBlob(status.text)
        sent = blob.sentiment
        polarity = sent.polarity
        subjectivity = sent.subjectivity

        if coords is not None:
            coords = json.dumps(coords)
        # Other Tweet Properties: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
        # Cool Doc examples:
            # includeretweet_count — the number of times a tweet has been retweeted.
            # withheld_in_countries — the tweet has been withheld in certain countries.
            # favorite_count — the number of times the tweet has been favorited by other users.

        # From Docs
        # The user's description (status.user.description). This is the description the user who created the tweet wrote in their biography.
        #     The user's location (status.user.location). This is the location the user who created the tweet wrote in their biography.
        #     The screen name of the user (status.user.screen_name).
        #     When the user's account was created (status.user.created_at).
        #     How many followers the user has (status.user.followers_count).
        #     The background color the user has chosen for their profile (status.user.profile_background_color).
        #     The text of the tweet (status.text).
        #     The unique id that Twitter assigned to the tweet (status.id_str).
        #     When the tweet was sent (status.created_at).
        #     How many times the tweet has been retweeted (status.retweet_count).
        #     The tweet's coordinates (status.coordinates). The geographic coordinates from where the tweet was sent.


        # Storing tweets into an SQLlite db so they can be easily queried, or dumped out to csv for further analysis.
        table.insert(dict(
            user_description=description,
            user_location=loc,
            coordinates=coords,
            text=text,
            user_name=name,
            user_created=user_created,
            user_followers=followers,
            id_str=id_str,
            created=created,
            retweet_count=retweets,
            user_bg_color=bg_color,
            polarity=sent.polarity,
            subjectivity=sent.subjectivity,
        ))
    # Override the on_error method of StreamListener so that we can handle errors coming from the Twitter API properly
    # The Twitter API will send a 420 status code if we're being rate limited. If this happens --> disconnect, any other error, keep going
    def on_error(self, status_code):
        if status_code == 420:
            return False




stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=["trump", "clinton", "hillary clinton", "donald trump"])
