# coding:utf-8
from slackclient import SlackClient
import time, datetime
import re
import plugins.function as f
import sys
sys.path.append('..')
import config

SC = SlackClient(config.slack_token)
prog = re.compile("^!get\s(\S+)\s*(.*)")
mention = re.compile("^<@U8211N9FW>\s(\S+)")
timedict = {}
days = "0101"
delTime = 300

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
        cmd = prog.match(dict["text"])
        msg = ""
        if cmd is not None:
            if "train" == cmd.group(1):
                #運行状況
                if "all" == cmd.group(2):
                    msg = f.traininfo("all")
                else:
                    msg = f.traininfo()
            elif "ktx" == cmd.group(1):
                if re.compile(r'[0-4][0-9]').search(cmd.group(2)):
                    username = ("3J" + cmd.group(2))
                    msg = ("\n")
                    msg += f.ktx(username)
                else:
                    msg = ("出席番号を入力してください")
            elif "duty" == cmd.group(1):
                msg = ("今週の日直は\n%sです" % f.touban(1))
            elif "clean" == cmd.group(1):
                msg = ("今週の掃除当番は\n%sです" % f.touban(0))
            elif "help" == cmd.group(1):
                msg = ("\n掃除当番[clean]\n日直[duty]\n鉄道運行状況[train (all)]\n北越[ktx]")
            elif "set" == cmd.group(1):
                if "U30T49610" == dict["user"]:
                    list = cmd.group(2).split(":")
                    if "deletetime" == list[0]:
                        global delTime
                        delTime = int(list[1])
                        msg = ("delTimeを" + str(delTime) + "に変更しました。")
                else:
                    msg = ("権限がありません")
            else:
                msg = ("コマンドが未登録です")

            user = dict["user"].encode("utf-8")
            res = sendSC("<@"+user+">:"+msg, dict["channel"])
            #削除用のtsを保存する
            global timedict
            timedict[res["ts"]] = res["channel"]
            #timedict[dict["ts"]] = dict["channel"]
        else:
            cmd = mention.match(dict["text"])
            if cmd is not None:
                #ドコモの人工知能に返信を任せる
                msg = f.docomo(cmd.group(1), config.docomo_apikey)
                user = dict["user"].encode("utf-8")
                sendSC("<@"+user+">:"+msg, dict["channel"])

def oneday():
    r = f.ktxDownload()
    """
    今日はm月d日(a) : 晴れ
    """
    if r is None:
        sendSC("J科サイトに接続できません。ktxが最新でない場合があります。", "C31GLQT47")

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
    res = SC.api_call(
        "chat.delete",
        channel = ch,
        ts = timeStump
        )
    return res

if __name__ == '__main__':
    if SC.rtm_connect():
        #接続開始
        #messageの時間取得用
        while True:
            now = datetime.datetime.now()
            #今日初めてかつ、7時代の時oneday実行
            if (now.strftime("%m%d")!= days) and (now.strftime("%H")== "07"):
                oneday()
                days = now.strftime("%m%d")
            main()
            #ここ削除
            for ts in timedict.keys():
                timeStump = int(ts.split(".")[0])
                timeStump = timeStump + delTime
                if int(time.time()) > timeStump:
                    r = delete(timedict[ts], ts)
                    del timedict[ts]
            time.sleep(1)
                
    else:
        pass