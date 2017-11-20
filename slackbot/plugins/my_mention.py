# coding: utf-8

from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
import re
import function as f

# @respond_to('string')     bot宛のメッセージ
# @listen_to('string')      チャンネル内のbot宛以外の投稿
# @default_reply()          DEFAULT_REPLY と同じ働き
# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する


@respond_to('help')
def mention_func(message):
    message.reply('cmd一覧:train, clean, duty')

@listen_to(r'^!get\s(\S+)\s*(.*)')
def listen(message, cmd, req):
    if cmd=='train':
        if req=="all":
            data = f.traininfo("all")
            msg = ""
            for i in data:
                msg += ("%s\n" %i)
            msg = msg.encode('utf-8')
            message.reply('運行状況\n%s' %msg)
        elif len(f.traininfo())==0:
            message.reply('乱れは無いようです...')
        else:
            msg = ""
	    data = f.traininfo()
            for i in data:
                msg += ("%s\n" %i)
            msg = msg.encode('utf-8')
            message.reply('遅延情報\n%s' %msg)
    elif cmd=='clean':
        message.reply('今週の掃除当番は\n%sです' % f.touban(0))
    elif cmd=='duty':
        message.reply('今週の日直は\n%sです' % f.touban(1))
    else :
        message.reply('NotCommand')
