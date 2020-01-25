import cardapioformatter as cf
import re
import tweepy
import time
from os import environ


CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
TOKEN = environ['TOKEN']
TOKEN_SECRET = environ['TOKEN_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(TOKEN, TOKEN_SECRET)

# Create API object
api = tweepy.API(auth)

botUser = '@bandejaobotufrj'


strings_ifcspv = cf.getCardapioCampus("IFCSPV")
strings_fundao = cf.getCardapioCampus("fundao")


def splitTweet(tweet):
    tweet1 = "\n".join(tweet.split("\n")[0:-4])
    tweet2 = tweet.split("\n", 6)[6]
    return [tweet1, tweet2]


def postAnswerTweets(tweetsCampus, user, idstring):

    introTweet = f'@{user.screen_name} Olá, {user.name}! Aqui está o cardápio:\n'

    if isinstance(tweetsCampus, list):
        for tweet in tweetsCampus:
            completeTweet = introTweet + tweet
            if len(completeTweet) >= 220:
                newTweets = splitTweet(completeTweet)
                print(newTweets)
                firstTweet = api.update_status(newTweets[0], idstring)
                api.update_status(f'{botUser}'+newTweets[1], firstTweet.id_str)
            else:
                print(completeTweet)
                api.update_status(completeTweet, idstring)

    else:
        completeTweet = introTweet + tweetsCampus
        if len(completeTweet) >= 220:
            newTweets = splitTweet(completeTweet)
            print(newTweets)
            firstTweet = api.update_status(newTweets[0], idstring)
            api.update_status(f'{botUser}'+newTweets[1], firstTweet.id_str)
        else:
            print(completeTweet)
            api.update_status(completeTweet, idstring)


def searchAndAnswer():

    myMentions = api.mentions_timeline(count=30)

    for mention in myMentions:

        if (hasattr(mention, 'retweeted_status') == False) and (hasattr(mention, 'quoted_status') == False) and not mention.favorited:

            almoco = re.search(r"\balmo(ç|c)o\b", mention.text, re.IGNORECASE)
            jantar = re.search(r"\bjantar\b", mention.text, re.IGNORECASE)
            fundao = re.search(r"\bfund(a|ã)o\b", mention.text, re.IGNORECASE)
            pvifcs = re.search(r"\b(pv|ifcs)\b", mention.text, re.IGNORECASE)

            if fundao:
                if almoco:
                    postAnswerTweets(
                        strings_fundao[0], mention.user, mention.id_str)
                elif jantar:
                    postAnswerTweets(
                        strings_fundao[1], mention.user, mention.id_str)
                else:
                    postAnswerTweets(
                        strings_fundao, mention.user, mention.id_str)
                api.create_favorite(mention.id)

            elif pvifcs:
                if almoco:
                    postAnswerTweets(
                        strings_ifcspv[0], mention.user, mention.id_str)
                elif jantar:
                    postAnswerTweets(
                        strings_ifcspv[1], mention.user, mention.id_str)
                else:
                    postAnswerTweets(
                        strings_ifcspv, mention.user, mention.id_str)
                api.create_favorite(mention.id)

            elif almoco:
                postAnswerTweets(
                    strings_ifcspv[0], mention.user, mention.id_str)
                postAnswerTweets(
                    strings_fundao[0], mention.user, mention.id_str)
                api.create_favorite(mention.id)

            elif jantar:
                postAnswerTweets(
                    strings_ifcspv[1], mention.user, mention.id_str)
                postAnswerTweets(
                    strings_fundao[1], mention.user, mention.id_str)
                api.create_favorite(mention.id)


while True:
    searchAndAnswer()
    print("done. Sleeping...")
    time.sleep(180)
    print("end of sleep")
