# coding: utf-8
# configのインポート
import sys
sys.path.append('..')
import config

# botアカウントのトークンを指定
API_TOKEN = config.slack_token

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = "!get hogeと話しかけてください"

# プラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ['plugins']
