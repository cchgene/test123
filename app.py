from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import random
import requests as r
from bs4 import BeautifulSoup as bs
from datetime import datetime 
import os
import mongodb

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['Access_Token'])

handler = WebhookHandler(os.environ['Secret'])

line_bot_api.push_message(os.environ['gene_uid'], TextSendMessage(text='買起來買起來'))

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'



@handler.add(FollowEvent)
def handle_follow(event):

    profile = line_bot_api.get_profile(event.source.user_id)
    name = profile.display_name
    uid = profile.user_id
    print(name)
    print(uid)
    
    if mongodb.find_user(uid,'vusers')<= 0:
        dic = {'userid':uid,
               'username':name,
               'creattime':datetime.now(),
               'Note':'user',
               'ready':0}
        mongodb.insert_one(dic,'vusers')

#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 取得個人資料
    profile = line_bot_api.get_profile(event.source.user_id)
    name = profile.display_name
    uid = profile.user_id
    message = event.message.text
    print(name)
    print(uid)
    print(message)
    
    dic = {'userid':uid,
           'username':name,
           'creattime':datetime.now(),
           'message':message}
        
    mongodb.insert_one(dic,'vmessages')
    
    if event.message.text == '抽圖':
        #line_picture = random.choice([[random.choice([i for i in range(1,18)] + [21] + [i for i in range(100,140)] + [i for i in range(401,431)]),1],[random.choice([18] + [19] + [20] + [i for i in range(22,48)] + [i for i in range(140,180)] + [i for i in range(501,528)]),2]])
        line_picture = random.choice([[random.choice([i for i in range(1,18)] + [21] + \
                               [i for i in range(100,140)] + [i for i in range(401,431)]),1],\
    [random.choice([18] + [19] + [20] + [i for i in range(22,48)] + \
                   [i for i in range(140,180)] + [i for i in range(501,528)]),2],\
    [random.choice([i for i in range(180,260)]),3],\
    [random.choice([i for i in range(260,308)] + \
                   [i for i in range(601,633)]),4]])
        message = StickerSendMessage(
            package_id=str(line_picture[1]),
            sticker_id=str(line_picture[0]))
        line_bot_api.reply_message(event.reply_token,message)

    elif event.message.text == '擲骰子':
        message = TextSendMessage(text=random.choice(['1','2','3','4','5','6']))
        line_bot_api.reply_message(event.reply_token,message)
    
    elif event.message.text[0] == '買':
        product = event.message.text[1:]
        dic = {'username':name,
           'creattime':datetime.now(),
           'product':product}
        mongodb.insert_one(dic,'vproduct')
    
    elif event.message.text[0:2] == '地址':
        address = event.message.text[2:]
        dic = {'username':name,
           'creattime':datetime.now(),
           'address':address}
        mongodb.insert_one(dic,'vprofile')
    
    elif event.message.text[0:2] == '電話':
        tel = event.message.text[2:]
        dic = {'username':name,
           'creattime':datetime.now(),
           'tel':tel}
        mongodb.insert_one(dic,'vprofile')
 
    elif event.message.text[0:2] == '稱呼':
        nam = event.message.text[2:]
        dic = {'username':name,
           'creattime':datetime.now(),
           'name':nam}
        mongodb.insert_one(dic,'vprofile')
    else:
        message = TextSendMessage(text=event.message.text[:2])
        
    line_bot_api.reply_message(event.reply_token,message)

if __name__ == '__main__':
    app.run(debug=True)
