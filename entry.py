# coding:utf-8
# ファミペイのrt応募を自動化する
import requests
import sys
import json
from requests_oauthlib import OAuth1Session
import config
from time import sleep
import re

pattern = r'^@taittide \n【残念。でもプレゼント！】'
checker = re.compile(pattern)

def main():
    url_mentions = "https://api.twitter.com/1.1/statuses/mentions_timeline.json"
    url_retweet = "https://api.twitter.com/1.1/statuses/retweet/1146917856187015168.json"
    url_unretweet = "https://api.twitter.com/1.1/statuses/unretweet/1146917856187015168.json"
    params = {"count": 1}
    while(True):
        res = oauth.post(url=url_retweet)
        if res.status_code == 200:
            print("rt ok!")
            sleep(10)
            res2 = oauth.get(url=url_mentions, params=params)
            mention = json.loads(res2.text)
            mention = mention[0]
            result = checker.match(mention["text"])
            if result:
                print("ハズレ...")
            else:
                print("finish!!!")
                return
            res3 = oauth.post(url_unretweet)
            if res3.status_code == 200:
                print("unrt ok!\n---------------")
            else:
                while(res3.status_code != 200):
                    res3 = oauth.post(url_unretweet)
                    sleep(5)
            sleep(26)
        else:
            print(res.status_code,res.text)
            sleep(60)


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

