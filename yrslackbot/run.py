# coding:utf-8
from slackclient import SlackClient
import time, datetime
import re
import plugins.function as f
import sys
sys.path.append('..')
import config

class Slackclient():
    timedict = {}
    def __init__(self):
        self.slackclient = SlackClient(config.slack_token)
        if not self.slackclient.rtm_connect():
            sys.exit()
    def reader(self):
        #readはdict型,SlackAPIの返り値
        self.read = self.slackclient.rtm_read()
        if self.read:
            self.read = self.read[0]
            return self.read
        else:
            return None
    def send(self, msg, ch, saveBool):
        res = self.slackclient.api_call(
                "chat.postMessage",
                channel = ch,
                text = msg,
                as_user = True
                )
        if saveBool == True:
            self.timesave(res)
        return res
    def reply(self, msg):
        res = self.slackclient.api_call(
                "chat.postMessage",
                channel = self.read["channel"],
                text = msg,
                as_user = True,
                thread_ts = self.read["ts"]
                )
        return res
    def sendMention(self, msg, saveBool):
        user = ("<@" + self.read["user"] + ">:")
        user = user.encode("utf-8")
        res = self.slackclient.api_call(
                "chat.postMessage",
                channel = self.read["channel"],
                text = (user + msg),
                as_user = True
                )
        if saveBool == True:
            self.timesave(res)
        return res
    def delete(self, saveTs):
        res = self.slackclient.api_call(
                "chat.delete",
                channel = self.timedict[saveTs],
                ts = saveTs
                )
        del self.timedict[saveTs]
        return res
    def timesave(self, res):
        self.timedict[res["ts"]] = res["channel"]

SC = Slackclient()
prog = re.compile("^!get\s(\S+)\s*(.*)")
mention = re.compile("^<@U8211N9FW>\s(\S+)")
days = "0101"
delTime = 300

def main():
    read = SC.reader()
    if read:
        #readがリストの場合があるがSlackclientで解決済み
        type = read.get("type")
        #type分岐[message]
        if "message" == type:
            message(read)
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
                    SC.sendMention(msg, True)
                elif "save" == cmd.group(2):
                    msg = f.traininfo()
                    SC.sendMention(msg, False)
                else:
                    msg = f.traininfo()
                    SC.sendMention(msg, True)
            elif "ktx" == cmd.group(1):
                if re.compile(r'[0-4][0-9]').search(cmd.group(2)):
                    username = ("3J" + cmd.group(2))
                    msg = ("\n")
                    msg += f.ktx(username)
                else:
                    msg = ("出席番号を入力してください")
                SC.sendMention(msg, True)
            elif "duty" == cmd.group(1):
                msg = ("今週の日直は\n%sです" % f.touban(1))
                SC.sendMention(msg, True)
            elif "clean" == cmd.group(1):
                msg = ("今週の掃除当番は\n%sです" % f.touban(0))
                SC.sendMention(msg, True)
            elif "help" == cmd.group(1):
                msg = ("\n掃除当番[clean]\n日直[duty]\n鉄道運行状況[train (all)]\n北越[ktx]")
                SC.sendMention(msg, True)
            elif "set" == cmd.group(1):
                if "U30T49610" == dict["user"]:
                    list = cmd.group(2).split(":")
                    if "deletetime" == list[0]:
                        global delTime
                        delTime = int(list[1])
                        msg = ("delTimeを" + str(delTime) + "に変更しました。")
                else:
                    msg = ("権限がありません")
                SC.sendMention(msg, True)
            else:
                msg = ("コマンドが未登録です")
                SC.sendMention(msg, True)
        else:
            cmd = mention.match(dict["text"])
            if cmd is not None:
                #ドコモの人工知能に返信を任せる
                msg = f.docomo(cmd.group(1), config.docomo_apikey)
                SC.sendMention(msg, False)

def oneday():
    r = f.ktxDownload()
    """
    今日はm月d日(a)
    >天気の情報
    >課題の情報
    """
    msg = ("今日は{}\n".format(now.strftime("%m月%d日(%a)")))
    msg += (">今日の天気[工事中]\n")
    msg += (">今日の課題[工事中]\n")
    SC.send(msg, "schedule", False)
    if r is None:
        SC.send("J科サイトに接続できません。ktxが最新でない場合があります。", "schedule", False)

if __name__ == '__main__':
    #接続開始
    #messageの時間取得用
    while True:
        now = datetime.datetime.now()
        #今日初めてかつ、7時代の時oneday実行
        if (now.strftime("%m%d")!= days) and (now.strftime("%H")== "06"):
            oneday()
            days = now.strftime("%m%d")
        main()
        #ここ削除
        for ts in SC.timedict.keys():
            timeStump = int(ts.split(".")[0])
            timeStump = timeStump + delTime
            if int(time.time()) > timeStump:
                SC.delete(ts)
        time.sleep(1)