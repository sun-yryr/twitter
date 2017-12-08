# coding:utf-8
from slackclient import SlackClient
import time
import re
import plugins.function as f
import sys
sys.path.append('..')
import config

SC = SlackClient(config.slack_token)
prog = re.compile("^!get\s(\S+)\s*(.*)")
timedict = {}

def main():
    global timeStump
    read = SC.rtm_read()
    #readがリストの場合がある
    for dict in read:
        type = dict.get("type")
        #type分岐[message]
        if "message" == type:
            message(dict)
        elif "c" == type:
            pass
        else:
            pass

def message(dict):
    #botによる返信を除外
    if ("subtype" in dict.keys()) or ("U8211N9FW" in dict.values()):
        pass
    else:
        #正規表現による!getとのマッチ
        result = prog.match(dict["text"])
        msg = ""
        if result is None:
            #コマンドを指示する？
            pass
        else:
            if "train" == result.group(1):
                #運行状況
                if "all" == result.group(2):
                    data = f.traininfo("all")
                    msg += ("運行状況\n")
                    for i in data:
                        i = i.encode("utf-8")
                        msg += ("%s\n" %i)
                elif len(f.traininfo())==0:
                    msg = ("乱れは無いようです...")
                else:
                    data = f.traininfo()
                    msg += ("遅延情報\n")
                    for i in data:
                        i = i.encode("utf-8")
                        msg += ("%s\n" %i)
            elif "ktx" == result.group(1):
                if re.compile(r'[0-4][0-9]').search(result.group(2)):
                    username = ("3J" + result.group(2))
                    msg = ("\n")
                    msg += f.ktx(username)
                else:
                    msg = ("出席番号を入力してください")
            elif "duty" == result.group(1):
                msg = ("今週の日直は\n%sです" % f.touban(1))
            elif "clean" == result.group(1):
                msg = ("今週の掃除当番は\n%sです" % f.touban(0))
            elif "help" == result.group(1):
                msg = ("\n掃除当番[clean]\n日直[duty]\n鉄道運行状況[train (all)]\n北越[ktx]")
            elif "set" == result.group(1):
                if "U30T49610" == dict["user"]:
                    msg = ("OK")
                else:
                    msg = ("権限がありません")
            else:
                msg = (result.group(1))

            user = dict["user"].encode("utf-8")
            res = sendSC("<@"+user+">:"+msg, dict["channel"])
            #削除用のtsを保存する
            global timedict
            timedict[res["ts"]] = res["channel"]

def sendSC(msg, ch):
    res = SC.api_call(
        "chat.postMessage",
        channel = ch,
        text = msg,
        as_user = True
        )
    return res
    
def replySC(msg, ch, timeStump):
    res = SC.api_call(
        "chat.postMessage",
        channel = ch,
        text = msg,
        as_user = True,
        thread_ts = timeStump
        )
    return res
    
def delete(ch, timeStump):
    SC.api_call(
        "chat.delete",
        channel = ch,
        ts = timeStump
    )

if __name__ == '__main__':
    if SC.rtm_connect():
        #接続開始
        #messageの時間取得用
        while True:
            main()
            now = int(time.time())
            for ts in timedict.keys():
                timeStump = int(ts.split(".")[0])
                timeStump = timeStump + 300
                if now > timeStump:
                    delete(timedict[ts], ts)
            time.sleep(1)
                
    else:
        pass