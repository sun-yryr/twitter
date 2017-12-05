# coding: utf-8
import sys
import os
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
            msg = mdSS.p.get_text()
            data.append("[*%s*]%s\n>%s" % (title, status, msg))
            #print ("[*%s*]%s\n%s" % (title, status, msg)
        else:
            pass

    return data

def ktx(usernumber):
    K_URL = "https://nittc.tokyo-ct.ac.jp/usr/kitakosi/LEE/PracProgI/"
    url = "https://nittc.tokyo-ct.ac.jp/xythoswfs/webui/_xy-e4168359_7-t_C5zhSCja"
    payload = {
        'password': '+81-42-668-5061'
    }
    retMsg = ""
    count = 1
    
    
    req = requests.session()
    req.post(url, data=payload)
    r = req.get(K_URL + "PracProgI_TOP.html")
    r = req.get(K_URL + "assignments/Check_Table.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    #<table border="1">を抽出
    alldata = soup.find_all("table", border="1")
    for list in reversed(alldata):
        #<tr>が1つしかなかったら対象ではないから除外
        tr = list.find_all("tr")
        if len(tr) > 1:
            #表の列数を取得する
            elements = len(tr[0].find_all("th"))
            retMsg += "[第" + str(count) + "回]"
            for user in tr:
                #引数で与えられた人の提出状況を確認
                if user.th.string == usernumber:
                    td = user.find_all("td")
                    #表の列数分ループ（列数3なら2回ループ-> 0-1のループなので-2する）
                    for i in range(elements-2):
                        if not isinstance(td[i].string, type(None)):
                            retMsg += td[i].string.encode("utf-8") + " "
                    else:
                        retMsg += "\n"
        count = count + 1
    return retMsg


#return msg
#msg = "http://traininfo.jreast.co.jp" + tr.img.get("src")
#return msg.encode('utf-8')
#traininfo()
