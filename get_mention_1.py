# coding:utf-8
# ファミペイのrt応募を自動化する
import requests
import sys
import json
from requests_oauthlib import OAuth1Session
import config
from time import sleep

def main():
    url_mentions = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    url_retweet = "https://api.twitter.com/1.1/statuses/retweet/1147182723179532288.json"
    url_unretweet = "https://api.twitter.com/1.1/statuses/unretweet/1147182723179532288.json"
    params = {"count": 1}
    res = oauth.get(url=url_mentions)
    if res.status_code == 200:
        fp = open("./test.json", "w")
        fp.write(res.text)
        fp.close()
    else:
        print(res.text)


if __name__ == '__main__':
    try:
        oauth = OAuth1Session(
                              config.Twi_CK,
                              config.Twi_CS,
                              config.Twi_AT,
                              config.Twi_ATS
                              )
    except:
        print("oauth error\n")
        sys.exit(1)
    
    main()

