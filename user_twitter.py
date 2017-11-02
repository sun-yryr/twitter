# coding:utf-8
#対象のツイートを通知、画像対応,
import requests
import sys
import json
from requests_oauthlib import OAuth1Session
import config

def main(oauth):
    url_tweet = "https://api.twitter.com/1.1/statuses/update.json"
    url_read = "https://api.twitter.com/1.1/statuses/home_timeline.json"
    url_myread = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    
    f = open("hdd1/dev/id.txt","r+")
    Twi_id = f.read()
    
    params = {
            "user_id":3404290100,
            "count":20,
            "since_id":Twi_id,
            "exclude_replies":True,
            "include_rts":False
        }
    req = oauth.get(url_myread, params = params)

    # レスポンスを確認
    if req.status_code == 200:
        timeline = json.loads(req.text)
        # 各ツイートの本文を表示
        for tweet in reversed(timeline):
            user = tweet["user"]
            toukou = "[" + user["name"] + "]\n" + tweet["text"]
            notify(toukou,None)

            try:
                entities = tweet["extended_entities"]
                for media in entities["media"]:
                    media_url = media["media_url"]
                    notify(media_url,media_url)
            except:
                madia_url = None
        if len(timeline) != 0:
            f.seek(0)
            f.write(tweet["id_str"])
    else:
        print ("Error: %d" % req.status_code)
    f.close


def notify(text,media_url):
    url = "https://notify-api.line.me/api/notify"
    token = config.LINE_token
    headers = {"Authorization" : "Bearer" + " " + token}
    payload = {
                "message" : text,
                "imageThumbnail" : media_url,
                "imageFullsize" : media_url
                }
    r = requests.post(url ,headers = headers ,params = payload)
    print r.status_code


if __name__ == '__main__':
    try:
        oauth = OAuth1Session(
                              config.Twi_CK,
                              config.Twi_CS,
                              config.Twi_AT,
                              config.Twi_ATS
                              )
    except:
        print "oauth error\n"
        sys.exit(1)
    
    main(oauth)

