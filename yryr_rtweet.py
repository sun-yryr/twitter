# coding:utf-8
import requests
from requests_oauthlib import OAuth1Session
import sys
import os
import json
import config
import re

def main():
    url_timeline = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    PATH = "/home/pi/hdd1/yryr_picture/"
    num = 1
    f = open(PATH + ".id", "r+")
    Twi_id = f.read()

    params = {
        "user_id": 410658466,
        "count": 20,
        "since_id": Twi_id,
        "include_rts": True
    }
    req = oauth.get(url_timeline, params = params)
    #レスポンス
    if req.status_code == 200:
        timeline = json.loads(req.text)
        for tweet in reversed(timeline):
            tweet_str = tweet["text"].encode("utf-8")
            rt_bool = tweet.get("retweeted")
            entities = tweet.get("extended_entities")
            if rt_bool and not entities is None:
                #print tweet_str
                for media in entities["media"]:
                    picture = requests.get(media["media_url_https"])
                    FILE_LIST = os.listdir(PATH)
                    #print FILE_LIST
                    name = "{0:03d}.png".format(num)
                    while name in FILE_LIST:
                            num = num + 1
                            name = "{0:03d}.png".format(num)
                            #print name
                    f2 = open(PATH + name, "w")
                    f2.write(picture.content)
                    f2.close()
        if len(timeline) != 0:
            f.seek(0)
            f.write(tweet["id_str"])
    else:
        print("Error: %d" % req.status_code)
    f.close()

    
if __name__ == '__main__':
    try:
        oauth = OAuth1Session(
            config.Twi_CK,
            config.Twi_CS,
            config.Twi_AT,
            config.Twi_ATS
        )
    except:
        print "oauth Error"
        sys.exit(1)
    main()