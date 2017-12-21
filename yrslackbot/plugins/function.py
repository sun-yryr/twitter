# coding: utf-8
import touban as T
from bs4 import BeautifulSoup
import requests
import json
import os
    
def touban(a):
    if a == "chenge":
        msg = T.main()
        return
    msg = T.m_print()
    #print -> slack.message
    if a == 0:
        return msg[0]
    else:
        return msg[1]

def traininfo(req=""):
    data = []
    urllist = ["https://transit.yahoo.co.jp/traininfo/detail/38/0/",
            "https://transit.yahoo.co.jp/traininfo/detail/102/0/",
            "https://transit.yahoo.co.jp/traininfo/detail/52/0/",
            "https://transit.yahoo.co.jp/traininfo/detail/31/0/"]
    for url in urllist:
        try:
            r = requests.get(url)
        except:
            return ("データを取得できませんでした。")
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
    if len(data) == 0:
        msg = ("乱れはないようです...")
    elif req == "all":
        msg = ("運行状況\n")
        for i in data:
            i = i.encode("utf-8")
            msg += (i + "\n")
    else:
        msg = ("遅延情報\n")
        for i in data:
            i = i.encode("utf-8")
            msg += (i + "\n")
    return msg

def ktxDownload():
    K_URL = "https://nittc.tokyo-ct.ac.jp/usr/kitakosi/LEE/PracProgI/"
    url = "https://nittc.tokyo-ct.ac.jp/xythoswfs/webui/_xy-e4168359_7-t_C5zhSCja"
    payload = {
        'password': '+81-42-668-5061'
    }
    req = requests.session()
    try:
        req.post(url, data=payload)
    except:
        return None
    r = req.get(K_URL + "assignments/Check_Table.html")
    r = r.text.encode("utf-8")
    FileName = os.getcwd()
    FileName += "/ktx.txt"
    f = open(FileName, "w")
    f.write(r)
    return "success"

def ktx(usernumber):
    retMsg = ""
    count = 1
    FileName = os.getcwd()
    FileName += "/ktx.txt"
    f = open(FileName, "r")
    
    soup = BeautifulSoup(f.read(), "html.parser")
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
                    for i in range(elements-1):
                        if not isinstance(td[i].get_text(), type(None)):
                            if i == (elements-2):
                                retMsg += "\n>" + td[i].get_text().encode("utf-8") + " "
                            else:
                                retMsg += td[i].get_text().encode("utf-8") + " "
                    else:
                        retMsg += "\n"
        count = count + 1
    return retMsg

def docomo(text, APIKEY):
    url = "https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue"
    payload = {"APIKEY": APIKEY}
    body = {"utt": text}
    res = requests.post(url, params=payload, data=json.dumps(body))
    jsondata = json.loads(res.text)
    return jsondata["utt"]
    
ktxDownload()