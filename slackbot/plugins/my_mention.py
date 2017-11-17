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


@respond_to(u'メンション')
def mention_func(message):
    message.reply('私にメンションと言ってどうするのだ')

@listen_to(r'^!get\s(\S+)')
def listen(message, cmd):
    print cmd
    if cmd=='train':
        message.reply('運行状況')
    elif cmd=='clean':
        message.reply('今週の掃除当番')
    else :
        message.reply('NotCommand')

@respond_to('Give me (.*)', re.IGNORECASE)
def giveme(message, something):
    message.reply('Here is {}'.format(something))
