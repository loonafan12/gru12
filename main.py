import requests
import tweepy
import os
import time
from datetime import date, datetime,timezone,timedelta
import json

MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'
POST_TWEET_URL = 'https://api.twitter.com/1.1/statuses/update.json'

Animal = {
    "2": "🐰", "3": "🐱", "4": "🕊", "5": "🐻", "6": "🦌", "7": "🦉",
    "8": "🐯", "9": "🐿", "10":"🦢", "11": "🐧", "12": "🦋", "13": "🐺"
}
Media = {
    "letter": "📸", "postcard": "📸"
}
fab = "https://vip-fab-api.myfab.tv/fapi/2/messages/"
headers = {
   "user-agent": "fab|ios|appstore|1.2.1|15.3.1|iPhone14,3|apple|ko|KR"
}
update = fab['messages'][0]

def thumbnail():
    requests.get(fab, headers=headers)

def twitter_api():
    access_token = '1540884453777866752-tN94jZPOwAAy4ZuJ0DuJcFg3ZLRov4'
    access_token_secret = 'S8EA4wN22wMGfTcgzsfZLofSNE1gf1qg1bamgknXB11pm'
    consumer_key = 'V4hxNVH5zEYJHUnu2fv2y8EHp'
    consumer_secret = 'x1Zaxa8qePWxn2OUGuHixWZcrTXCD7ihqJi4Vrfydkew8vR8tR'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def tweet_image(url, message):
    api = twitter_api()
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request.iter_content(chunk_size=1024**2):
                image.write(chunk)
        api.update_with_media(filename, status=message)
        os.remove(filename)
    else:
        filename.append(str(url))
        print("Unable to download image")

while True:
    if str(update['userId']) in Animal:
        emoji = Animal.get(str(update['userId']))
        format = datetime.fromtimestamp(update['publishedAt']/1000,timezone.utc).astimezone(timezone(timedelta(hours=9),name="KST")).strftime("%y%m%d %H:%M")
        url = update['letter']['thumbnail']
        message = "[" + emoji + "📸" + "]" + "" + format
        tweet_image(url, message)
    else:
        print("error")
    time.sleep(60)
