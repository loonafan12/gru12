import requests
import tweepy
import os
import time
from datetime import date, datetime,timezone,timedelta
import json
import re
from requests_oauthlib import OAuth1

animal = {
    "2": "🐰", "3": "🐱", "5": "🐻", "6": "🦌", "7": "🦉",
    "8": "🐯", "9": "🐿", "10":"🦢", "11": "🐧", "12": "🦋", "13": "🐺"
}

headers = {
   "user-agent": "fab|ios|appstore|1.2.1|15.3.1|iPhone14,3|apple|ko|KR",
   "accesstoken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NUb2tlbiI6IjViNjE2ZTg2M2FjZDRlZjg1ZjIwMDFkMTQ5MWVhNDg0ZTY1ZTg5YmIyMzYwODkwNTkyOTRkZDUwNWY5MjgzOGMiLCJpZCI6MzUxNTIsImlhdCI6MTY0ODYxMDI0Mn0.Pk-bCiH9ENHaH2kBwpu1QZVcWoQGuAUOA_WaetmOOtk"
}

web_auth = OAuth1(
            client_key = "F1Q7dArYLKenUGGJMctt5VxCb", #api
            client_secret = "JuG3RwsOsM2hNm4ie1ONnaqI98eDwTX2EqydTQCr1X7i1tAYo0", #api secret
            resource_owner_key = "1495430246077636612-46XzlWtFtjsSePQLmXthG6nEKAvfBL", #access
            resource_owner_secret = "1RLjqh3McaPEX78llSsQDQ12fFbJ6lNQHJwhCAZ9mtXSG") #access secret

upload_url = 'https://upload.twitter.com/1.1/media/upload.json'
tweet_url = 'https://api.twitter.com/1.1/textes/update.json'

def fab():
    fab = requests.get("https://vip-fab-api.myfab.tv/fapi/2/messages", headers=headers)
    update = fab.json()['messages'][0]
    return update

def get_format(update):
    print("fetching captions...")
    emoji = animal.get(str(update['userId']))
    time_1 = datetime.fromtimestamp(update['publishedAt']/1000,timezone.utc).astimezone(timezone(timedelta(hours=9),name="KST")).strftime("%y%m%d %H:%M")
    time_2 = datetime.fromtimestamp(update['publishedAt']/1000,timezone.utc).astimezone(timezone(timedelta(hours=-4),name="EDT")).strftime("%y%m%d %H:%M")
    if "letter" in update:
        url = update['letter']['thumbnail']
        message = f"[{emoji}📸] {time_1} KST ({time_2} EDT)"
    else:
        url = update['postcard']['thumbnail']
        message = f"[{emoji}🎥] {time_1} KST ({time_2} EDT)"
    return message

def get_captions(update):
    num = update['id']
    fab = requests.get(f"https://vip-fab-api.myfab.tv/fapi/2/users/35152/message/{num}", headers=headers)
    fab = json.loads(fab.json()['message']['letter']['text'])
    update = fab['contents']
    output = []
    for txt in update:
        try:                                                                        
            if txt['type'] == "text":
                output.append(f"{txt['text']}")
            elif txt['type'] == "image":
                output.append(f"\n")
        except:
            output.append(" ")
    return output

def rename(update):
    print("generating links...")
    if "letter" in update:
        thumbnail = update['letter']['thumbnail']
        format = re.findall(r"(.*\/)", thumbnail)
        format = format [0]
        thumbnail = re.findall(r"(\d{10,14})", thumbnail)
        for num in range (-1, 2):
            n1 = int(thumbnail[0]) + num
            for num in range (-1 , 2):
                n2 = int (thumbnail[1]) + num
                multiply = 0
                for times in range (1, 13):
                    multiply += 1
                    link = f"{format}{n1}_{n2}_{multiply}_f.jpg"
                    media.append(link)
    if "postcard" in update:
        thumbnail = update['postcard']['thumbnail']
        format = re.findall(r"(.*\/)", thumbnail)
        format = format [0]
        thumbnail = re.findall(r"(\d{10,14})", thumbnail)
        for num in range (-1, 2):
            n1 = int(thumbnail[0]) + num
            for num in range (-1 , 2):
                n2 = int (thumbnail[1]) + num
                multiply = [".jpg", ".mp4"]
                for type in multiply:
                    link = f"{format}{n1}_{n2}_f{type}"
                    media.append(link)

def twitter_api():
    client = tweepy.Client(
        access_token="1495430246077636612-46XzlWtFtjsSePQLmXthG6nEKAvfBL",
        access_token_secret="1RLjqh3McaPEX78llSsQDQ12fFbJ6lNQHJwhCAZ9mtXSG",
        consumer_key="F1Q7dArYLKenUGGJMctt5VxCb",
        consumer_secret="JuG3RwsOsM2hNm4ie1ONnaqI98eDwTX2EqydTQCr1X7i1tAYo0",
        bearer_token = "AAAAAAAAAAAAAAAAAAAAANzcgAEAAAAAi28X4uCZMS35gknW2mD%2FYZCE33E%3DAJCYw3ttmstH1Ck35TPrL6hD7bnybatpKPy71EjlGsEBQcZmK0")

    # auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    return client

def init_media(filename):
    if ".jpg" in filename:
        request_data = {
        'command': 'INIT',
        'total_bytes': os.path.getsize(filename),
        'media_type': 'image/jpeg',
        'media_category': 'tweet_image'
        } 
        headers = {
        'content-type': 'application/octet-stream'
        }
        request = requests.post(url=upload_url, params=headers, data=request_data, auth=web_auth)
        test = request.json()
    else:
        request_data = {
        'command': 'INIT',
        'total_bytes': os.path.getsize(filename),
        'media_type': 'video/mp4',
        'media_category': 'tweet_video'
        }
        request = requests.post(url=upload_url, data=request_data, auth=web_auth)
        test = request.json()
    media_id = request.json()['media_id']
    return media_id

def append_media(media_id, file):
    print("uploading...")
    segment_id = 0
    bytes_sent = 0
    total_bytes= os.path.getsize(file)
    file = open(file, 'rb')
    while bytes_sent < total_bytes:
        chunk = file.read(4*1024*1024)
        request_data = {
        'command': 'APPEND',
        'media_id': media_id,
        'segment_index': segment_id
        }
        files = {
        'media':chunk
        }
        request = requests.post(url=upload_url, data=request_data, files=files, auth=web_auth)
        segment_id = segment_id + 1
        bytes_sent = file.tell()
        print("%s of %s bytes uploaded" % (str(bytes_sent), str(total_bytes)))

def finalize_video(media_id):
    print("finalizing video...")
    state = ""
    while state != "succeeded":
        request_data = {
            'command': 'FINALIZE',
            'media_id': media_id,
            'allow_async': 'true'
        }
        request = requests.post(url=upload_url, data=request_data, auth=web_auth)
        state = request.json()['processing_info']['state']
        request_params = {
            'command': 'STATUS',
            'media_id': media_id
        }
        request = requests.get(url=upload_url, params=request_params, auth=web_auth)
        state = request.json()['processing_info']['state']
    return state

def finalize_image(media_id):
    request_data = {
        'command': 'FINALIZE',
        'media_id': media_id,
    }
    request = requests.post(url=upload_url, data=request_data, auth=web_auth)

# update = fab()
# check = get_format(update)
# print(check)
while True:
    media = []
    media_ids = []
    update = fab()
    format = get_format(update)
    if str(update['userId']) in animal:
        if format != check:
            rename(update)
            list(dict.fromkeys(media))
            for links in media:
                request = requests.get(links, stream=True)
                if request.status_code == 200:
                    print("downloading...")
                    file = str(links).split("/")
                    file = file[6]
                    with open(file, 'wb') as image:
                        for chunk in request:
                            image.write(chunk)
                    media_id = init_media(file)
                    media_ids.append(media_id)
                    append_media(media_id, file)
                    if ".mp4" in file:
                        finalize_video(media_id)
                    else:
                        finalize_image(media_id)
                    filename = str(file)
                    os.remove(file)
            print("tweeting...")
            client = twitter_api()
            if ".jpg" in filename:
                count = len(media_ids)
                captions = get_captions(update)
                c0 = f"{format}\n\n{''.join(captions)}"
                c1 = f"{format}\n\n{''.join(captions[0:int(len(captions)/2)])}"
                c2 = f"{format}\n\n{''.join(captions[int(len(captions)/2):int(len(captions))])}"
                c3 = f"{format}\n\n{''.join(captions[0:int(round(len(captions)/3))])}"
                c4 = f"{format}\n\n{''.join(captions[int(round(len(captions)/3)):int(round(len(captions)/3)*2)])}"
                c5 = f"{format}\n\n{''.join(captions[int(round(len(captions)/3)*2):int(len(captions))])}"
                if count < 5 and len(c0) <= 200:
                    tweet = update_text = client.create_tweet(text=c0, media_ids=media_ids, reply_settings="following")
                elif count < 5 and len(c0) >= 400:
                    if len(' '.join(captions)) % 2 == 0:
                        tweet = client.create_tweet(text=c1, media_ids=media_ids, reply_settings="following")
                        thread_id = re.findall(r"\d{19}",str(tweet))
                        thread_id = thread_id[0]
                        tweet = client.create_tweet(text=c2, in_reply_to_tweet_id=thread_id)
                    else:
                        tweet = client.create_tweet(text=c3, media_ids=media_ids, reply_settings="following")
                        thread_id = re.findall(r"\d{19}",str(tweet))
                        thread_id = thread_id[0]
                        tweet = client.create_tweet(text=c4, in_reply_to_tweet_id=thread_id)
                        thread_id = re.findall(r"\d{19}",str(tweet))
                        thread_id = thread_id[0]
                        tweet = client.create_tweet(text=c5, in_reply_to_tweet_id=thread_id)
                elif count < 9:
                    if count == 6 and len(c0) <= 250:
                        tweet = client.create_tweet(text=c0, media_ids=media_ids[0:3], reply_settings="following")
                        thread_id = re.findall(r"\d{19}",str(tweet))
                        thread_id = thread_id[0]
                        tweet = client.create_tweet(text=format, media_ids=media_ids[3:count], in_reply_to_tweet_id=thread_id)
                    elif count == 6 and len(c0) >= 250:
                        if len(' '.join(captions)) % 2 == 0:
                            tweet = client.create_tweet(text=c1, media_ids=media_ids[0:3], reply_settings="following")
                            thread_id = re.findall(r"\d{19}",str(tweet))
                            thread_id = thread_id[0]
                            tweet = client.create_tweet(text=c2, media_ids=media_ids[3:count], in_reply_to_tweet_id=thread_id)
                        else:
                            tweet = client.create_tweet(text=c3, media_ids=media_ids[0:3], reply_settings="following")
                            thread_id = re.findall(r"\d{19}",str(tweet))
                            thread_id = thread_id[0]
                            tweet = client.create_tweet(text=c4, media_ids=media_ids[3:count], in_reply_to_tweet_id=thread_id)
                            thread_id = re.findall(r"\d{19}",str(tweet))
                            thread_id = thread_id[0]
                            tweet = client.create_tweet(text=c5, in_reply_to_tweet_id=thread_id)
                    elif count != 6 and len(c0) <= 250:
                        tweet = client.create_tweet(text=c0, media_ids=media_ids[0:4], reply_settings="following")
                        thread_id = re.findall(r"\d{19}",str(tweet))
                        thread_id = thread_id[0]
                        tweet = client.create_tweet(text=format, media_ids=media_ids[4:count], in_reply_to_tweet_id=thread_id)
                    else:
                        if len(' '.join(captions)) % 2 == 0:
                            tweet = client.create_tweet(text=c1, media_ids=media_ids[0:4], reply_settings="following")
                            thread_id = re.findall(r"\d{19}",str(tweet))
                            thread_id = thread_id[0]
                            tweet = client.create_tweet(text=c2, media_ids=media_ids[4:count], in_reply_to_tweet_id=thread_id)
                        else:
                            tweet = client.create_tweet(text=c3, media_ids=media_ids[0:4], reply_settings="following")
                            thread_id = re.findall(r"\d{19}",str(tweet))
                            thread_id = thread_id[0]
                            tweet = client.create_tweet(text=c4, media_ids=media_ids[4:count], in_reply_to_tweet_id=thread_id)
                            thread_id = re.findall(r"\d{19}",str(tweet))
                            thread_id = thread_id[0]
                            tweet = client.create_tweet(text=c5, in_reply_to_tweet_id=thread_id)
                else:
                    if len(c0) < 250:
                        tweet = client.create_tweet(text=c0, media_ids=media_ids[0:4], reply_settings="following")
                        thread_id = re.findall(r"\d{19}",str(tweet))
                        thread_id = thread_id[0]
                        tweet = client.create_tweet(text=format, media_ids=media_ids[4:8], in_reply_to_tweet_id=thread_id)
                        thread_id = re.findall(r"\d{19}",str(tweet))
                        thread_id = thread_id[0]
                        tweet = client.create_tweet(text=format, media_ids=media_ids[8:count], in_reply_to_tweet_id=thread_id)
                    else:
                        if len(' '.join(captions)) % 2 == 0:
                            tweet = client.create_tweet(text=c1, media_ids=media_ids[0:4], reply_settings="following")
                            thread_id = re.findall(r"\d{19}",str(tweet))
                            thread_id = thread_id[0]
                            tweet = client.create_tweet(text=c2, media_ids=media_ids[4:8], in_reply_to_tweet_id=thread_id)
                            thread_id = re.findall(r"\d{19}",str(tweet))
                            thread_id = thread_id[0]
                            tweet = client.create_tweet(text=format, media_ids=media_ids[8:count], in_reply_to_tweet_id=thread_id)
                        else:
                            tweet = client.create_tweet(text=c3, media_ids=media_ids[0:4], reply_settings="following")
                            thread_id = re.findall(r"\d{19}",str(tweet))
                            thread_id = thread_id[0]
                            tweet = client.create_tweet(text=c4, media_ids=media_ids[4:8], in_reply_to_tweet_id=thread_id)
                            thread_id = re.findall(r"\d{19}",str(tweet))
                            thread_id = thread_id[0]
                            tweet = client.create_tweet(text=c5, media_ids=media_ids[8:count], in_reply_to_tweet_id=thread_id)
            else:
                tweet = client.create_tweet(text=format, media_ids=media_ids, reply_settings="following")
                print(tweet)
            check = re.findall(r"\[.{38}\)", str(tweet))
            check = check[0]
            print("a new tweet has been uploaded")
        else:
            print("this tweet already exist")
    else:
        print("not loona")
    print("retrying...")
    time.sleep(3)
