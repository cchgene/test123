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
        if event.message.text == '買':
            message = TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/qnACcLd.jpg',
                        title='綜合營養組合',
                        text='幫妳配好好的組合，再也不用再擔心不知道吃什麼',
                        actions=[
                            MessageTemplateAction(
                                label='鮮蔬果組',
                                text='鮮蔬果組'
                            ),
                            MessageTemplateAction(
                                label='當季蔬果組',
                                text='當季蔬果組'
                            ),
                            MessageTemplateAction(
                                label='綠色蔬菜組',
                                text='綠色蔬菜組'
                            )
                        ]
                    ),
                        CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/0xFDvDV.jpg',
                        title='節慶組合',
                        text='節慶必備(烤肉、拜拜)',
                        actions=[
                            MessageTemplateAction(
                                label='烤肉組合',
                                text='烤肉組合'
                            ),
                            MessageTemplateAction(
                                label='拜拜組合',
                                text='拜拜組合'
                            ),
                            MessageTemplateAction(
                                label='任意組合',
                                text='任意組合'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/cLRmBTe.jpg',
                        title='其他',
                        text='其他',
                        actions=[
                            MessageTemplateAction(
                                label='關於鮮蔬盒',
                                text='關於鮮蔬盒'
                            ),
                            MessageTemplateAction(
                                label='菜單與分類',
                                text='菜單與分類'
                            ),
                            MessageTemplateAction(
                                label='其他',
                                text='其他'
                            )
                        ]
                    )
                ]
            )
        )
        else:
            product = event.message.text[1:]
            dic = {'username':name,
               'creattime':datetime.now(),
               'product':product}
            mongodb.insert_one(dic,'vproduct')
            message = TextSendMessage(text='小鮮盒已經收到囉~~還要其他的嗎?')
            name_active = str(name)+':'+str(event.message.text)
            line_bot_api.push_message(os.environ['gene_uid'], TextSendMessage(text=name_active))
        line_bot_api.reply_message(event.reply_token,message)
    elif event.message.text[0:2] == '地址':
        address = event.message.text[2:]
        dic = {'username':name,
           'creattime':datetime.now(),
           'address':address}
        mongodb.insert_one(dic,'vprofile')
        message = TextSendMessage(text='小鮮盒把地址記起來囉')
        line_bot_api.reply_message(event.reply_token,message)
        name_active = str(name)+':'+str(event.message.text)
        line_bot_api.push_message(os.environ['gene_uid'], TextSendMessage(text=name_active))
    elif event.message.text[0:2] == '電話':
        tel = event.message.text[2:]
        dic = {'username':name,
           'creattime':datetime.now(),
           'tel':tel}
        mongodb.insert_one(dic,'vprofile')
        message = TextSendMessage(text='小鮮盒把電話記起來囉')
        line_bot_api.reply_message(event.reply_token,message)
        name_active = str(name)+':'+str(event.message.text)
        line_bot_api.push_message(os.environ['gene_uid'], TextSendMessage(text=name_active))
    elif event.message.text[0:2] == '稱呼':
        nam = event.message.text[2:]
        dic = {'username':name,
           'creattime':datetime.now(),
           'name':nam}
        mongodb.insert_one(dic,'vprofile')
        message = TextSendMessage(text='小鮮盒把稱呼記起來囉')
        line_bot_api.reply_message(event.reply_token,message)
        name_active = str(name)+':'+str(event.message.text)
        line_bot_api.push_message(os.environ['gene_uid'], TextSendMessage(text=name_active))

    else:
        dic = {'userid':uid,
           'username':name,
           'creattime':datetime.now(),
           'message':message}
        
        mongodb.insert_one(dic,'vmessages')
        name_active = str(name)+':'+str(event.message.text)
        line_bot_api.push_message(os.environ['gene_uid'], TextSendMessage(text=name_active))
    #    message = TextSendMessage(text=event.message.text[:2])
        
    #line_bot_api.reply_message(event.reply_token,message)

if __name__ == '__main__':
    app.run(debug=True)
