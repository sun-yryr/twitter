# coding:utf-8
import requests
from requests_oauthlib import OAuth1Session
import sys
import os
import json
import config

def main():
    url_timeline = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    PATH = "/home/pi/hdd1/yryr_picture/"
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
                re_status = tweet["retweeted_status"]
                re_user = re_status["user"]
                re_name = re_user["screen_name"].encode("utf-8")
                if not re_name in os.listdir(PATH):
                    os.makedirs(PATH + re_name)
                path = PATH + re_name + "/"
                #print tweet_str
                num = 1
                for media in entities["media"]:
                    picture = requests.get(media["media_url_https"])
                    FILE_LIST = os.listdir(path)
                    #print FILE_LIST
                    name = re_name+"_{0:04d}.png".format(num)
                    while name in FILE_LIST:
                            num = num + 1
                            name = re_name+"_{0:04d}.png".format(num)
                            #print name
                    f2 = open(path + name, "w")
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