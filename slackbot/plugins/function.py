# coding: utf-8
import sys,os
sys.path.append(os.pardir)
import touban as T
from bs4 import BeautifulSoup
import requests

def touban(a):
    msg = T.m_print()
    #print -> slack.message
    if a==0:
        return msg[0]
    else:
        return msg[1]

def traininfo(req=""):
    data = []
    urllist = ["https://transit.yahoo.co.jp/traininfo/detail/38/0/",
            "https://transit.yahoo.co.jp/traininfo/detail/102/0/",
            "https://transit.yahoo.co.jp/traininfo/detail/52/0/",
            "https://transit.yahoo.co.jp/traininfo/detail/31/0/"]
    for (i, url) in enumerate(urllist):
        r = requests.get(url)
        #スクレイビング
        soup = BeautifulSoup(r.text, "html.parser")
        main = soup.find("div", class_="mainWrp")
        #decompose() -> 内容含めタグ削除
        mdSS = main.find(id="mdServiceStatus")
        mdSS.dt.span.decompose()
        status = mdSS.dt.get_text()
        status = status.replace("\n","")
        if status!=(u"平常運転") or req=="all":
            title = main.find(class_="title").string
            note = mdSS.p.get_text()
            data.append("[*%s*]%s\n>%s" % (title, status, note))
            #print ("[*%s*]%s\n%s" % (title, status, note))
        else:
            pass

    return data
#return msg
#msg = "http://traininfo.jreast.co.jp" + tr.img.get("src")
#return msg.encode('utf-8')
#traininfo()
