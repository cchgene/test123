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
        add_mes = str(name) + '已經加入小鮮盒囉'
        line_bot_api.push_message(os.environ['gene_uid'], TextSendMessage(text=add_mes))

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    name = profile.display_name
    uid = profile.user_id
    message = event.message.text
    print(name)
    print(uid)
    print(message)
    
    if event.message.text[0:4] == '買鮮蔬果':
        if event.message.text[4] == '大':
            combo_product = event.message.text[1:7]
            combo_count = event.message.text[-1]
        elif event.message.text[4] == '中':
            combo_product = event.message.text[1:7]
            combo_count = event.message.text[-1]
        elif event.message.text[4] == '小':
            combo_product = event.message.text[1:7]
            combo_count = event.message.text[-1]
        dic = {'userid':uid,
            'username':name,
            'creattime':datetime.now(),
            'product':combo_product,
            'count':combo_count,
            'status':0}
        mongodb.insert_one(dic,'vproduct')
        message = TextSendMessage(text='小鮮盒已經收到囉~~還要其他的嗎?')
        name_active = str(name)+':'+str(event.message.text)
        line_bot_api.push_message(os.environ['gene_uid'], TextSendMessage(text=name_active))
        line_bot_api.reply_message(event.reply_token,message)

    elif event.message.text[0:5] == '買當季蔬果':
        if event.message.text[5] == '大':
            combo_product = event.message.text[1:8]
            combo_count = event.message.text[-1]
        elif event.message.text[5] == '中':
            combo_product = event.message.text[1:8]
            combo_count = event.message.text[-1]
        elif event.message.text[5] == '小':
            combo_product = event.message.text[1:8]
            combo_count = event.message.text[-1]
        dic = {'userid':uid,
            'username':name,
            'creattime':datetime.now(),
            'product':combo_product,
            'count':combo_count,
            'status':0}
        mongodb.insert_one(dic,'vproduct')
        message = TextSendMessage(text='小鮮盒已經收到囉~~還要其他的嗎?')
        name_active = str(name)+':'+str(event.message.text)
        line_bot_api.push_message(os.environ['gene_uid'], TextSendMessage(text=name_active))
        line_bot_api.reply_message(event.reply_token,message)

    elif event.message.text[0:5] == '買綠色蔬菜':
        if event.message.text[5] == '大':
            combo_product = event.message.text[1:8]
            combo_count = event.message.text[-1]
        elif event.message.text[5] == '中':
            combo_product = event.message.text[1:8]
            combo_count = event.message.text[-1]
        elif event.message.text[5] == '小':
            combo_product = event.message.text[1:8]
            combo_count = event.message.text[-1]
        dic = {'userid':uid,
            'username':name,
            'creattime':datetime.now(),
            'product':combo_product,
            'count':combo_count,
            'status':0}
        mongodb.insert_one(dic,'vproduct')
        message = TextSendMessage(text='小鮮盒已經收到囉~~還要其他的嗎?')
        name_active = str(name)+':'+str(event.message.text)
        line_bot_api.push_message(os.environ['gene_uid'], TextSendMessage(text=name_active))
        line_bot_api.reply_message(event.reply_token,message)

    elif event.message.text[0:3] == '買烤肉':
        if event.message.text[3] == '大':
            combo_product = event.message.text[1:6]
            combo_count = event.message.text[-1]
        elif event.message.text[3] == '中':
            combo_product = event.message.text[1:6]
            combo_count = event.message.text[-1]
        elif event.message.text[3] == '小':
            combo_product = event.message.text[1:6]
            combo_count = event.message.text[-1]
        dic = {'userid':uid,
            'username':name,
            'creattime':datetime.now(),
            'product':combo_product,
            'count':combo_count,
            'status':0}
        mongodb.insert_one(dic,'vproduct')
        message = TextSendMessage(text='小鮮盒已經收到囉~~還要其他的嗎?')
        name_active = str(name)+':'+str(event.message.text)
        line_bot_api.push_message(os.environ['gene_uid'], TextSendMessage(text=name_active))
        line_bot_api.reply_message(event.reply_token,message)

    elif event.message.text[0:3] == '買拜拜':
        if event.message.text[3] == '大':
            combo_product = event.message.text[1:6]
            combo_count = event.message.text[-1]
        elif event.message.text[3] == '中':
            combo_product = event.message.text[1:6]
            combo_count = event.message.text[-1]
        elif event.message.text[3] == '小':
            combo_product = event.message.text[1:6]
            combo_count = event.message.text[-1]
        dic = {'userid':uid,
            'username':name,
            'creattime':datetime.now(),
            'product':combo_product,
            'count':combo_count,
            'status':0}
        mongodb.insert_one(dic,'vproduct')
        message = TextSendMessage(text='小鮮盒已經收到囉~~還要其他的嗎?')
        name_active = str(name)+':'+str(event.message.text)
        line_bot_api.push_message(os.environ['gene_uid'], TextSendMessage(text=name_active))
        line_bot_api.reply_message(event.reply_token,message)

    elif event.message.text == '查詢訂單':
        product_list = mongodb.get_user_product(uid,'vproduct')
        if len(product_list) == 0:
            message = TextSendMessage(text='目前並無商品')
        else:
            message = '\n'.join(('目前購買 '+i[0]+' 共 '+i[1]+' 份' for i in dict(product_list).items()))
            #message = str(dict(product_list))
            print(message)
            message = TextSendMessage(text=message)

        line_bot_api.reply_message(event.reply_token,message)

    elif event.message.text == '刪除購物籃內所有組合商品':
        mongodb.remove_user_product(uid,'vproduct')
        message = TextSendMessage(text='已刪除購物車內所有組合商品')
        line_bot_api.reply_message(event.reply_token,message)
        name_active = str(name)+':'+str(event.message.text)
        line_bot_api.push_message(os.environ['gene_uid'], TextSendMessage(text=name_active))

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

    elif event.message.text == '鮮蔬果組': 
        message = TemplateSendMessage(
                alt_text='需要哪種鮮蔬果組合呢?',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/qnACcLd.jpg',
                        title='需要哪種鮮蔬果組合呢?',
                        text='包含各式葉菜、根莖、菇菌、瓜果、豆以及(蔥、薑、蒜、辣椒)調味類',
                        actions=[
                            MessageTemplateAction(
                            label='大組合-299元(4-5人份)',
                            text='買鮮蔬果大組合X1'
                            ),
                            MessageTemplateAction(
                            label='中組合-199元(2-3人份)',
                            text='買鮮蔬果中組合X1'
                            ),
                            MessageTemplateAction(
                            label='小組合-99元(1-2人份)',
                            text='買鮮蔬果小組合X1'
                            )])]))
        line_bot_api.reply_message(event.reply_token,message)

    elif event.message.text == '當季蔬果組': 
        message = TemplateSendMessage(
                alt_text='需要哪種當季蔬果組合呢?',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/qnACcLd.jpg',
                        title='需要哪種當季蔬果組合呢?',
                        text='包含當季葉菜、根莖、菇菌、瓜果、豆以及(蔥、薑、蒜、辣椒)調味類',
                        actions=[
                            MessageTemplateAction(
                            label='大組合-299元(4-5人份)',
                            text='買當季蔬果大組合X1'
                            ),
                            MessageTemplateAction(
                            label='中組合-199元(2-3人份)',
                            text='買當季蔬果中組合X1'
                            ),
                            MessageTemplateAction(
                            label='小組合-99元(1-2人份)',
                            text='買當季蔬果小組合X1'
                            )])]))
        line_bot_api.reply_message(event.reply_token,message)

    elif event.message.text == '綠色蔬菜組': 
        message = TemplateSendMessage(
                alt_text='需要哪種綠色蔬菜組合呢?',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/qnACcLd.jpg',
                        title='需要哪種綠色蔬菜組合呢?',
                        text='由不同的綠色蔬菜所組成(至少2-3種以上)',
                        actions=[
                            MessageTemplateAction(
                            label='大組合-299元(4-5人份)',
                            text='買綠色蔬菜大組合X1'
                            ),
                            MessageTemplateAction(
                            label='中組合-199元(2-3人份)',
                            text='買綠色蔬菜中組合X1'
                            ),
                            MessageTemplateAction(
                            label='小組合-99元(1-2人份)',
                            text='買綠色蔬菜小組合X1'
                            )])]))
        line_bot_api.reply_message(event.reply_token,message)

    elif event.message.text == '烤肉組合': 
        message = TemplateSendMessage(
                alt_text='需要哪種烤肉組合呢?',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/qnACcLd.jpg',
                        title='需要哪種烤肉組合呢?',
                        text='由不同的烤肉必備食材所組成(至少2-3種以上)',
                        actions=[
                            MessageTemplateAction(
                            label='大組合-299元(4-5人份)',
                            text='買烤肉大組合X1'
                            ),
                            MessageTemplateAction(
                            label='中組合-199元(2-3人份)',
                            text='買烤肉中組合X1'
                            ),
                            MessageTemplateAction(
                            label='小組合-99元(1-2人份)',
                            text='買烤肉小組合X1'
                            )])]))
        line_bot_api.reply_message(event.reply_token,message)

    elif event.message.text == '拜拜組合': 
        message = TemplateSendMessage(
                alt_text='需要哪種拜拜組合呢?',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/qnACcLd.jpg',
                        title='需要哪種拜拜組合呢?',
                        text='由各個節日拜拜所需蔬果組成(至少2-3種以上)',
                        actions=[
                            MessageTemplateAction(
                            label='大組合-299元(4-5人份)',
                            text='買拜拜大組合X1'
                            ),
                            MessageTemplateAction(
                            label='中組合-199元(2-3人份)',
                            text='買拜拜中組合X1'
                            ),
                            MessageTemplateAction(
                            label='小組合-99元(1-2人份)',
                            text='買拜拜小組合X1'
                            )])]))
        line_bot_api.reply_message(event.reply_token,message)

    elif event.message.text == '買':
        message = TemplateSendMessage(
            alt_text='買什麼東西呢?',
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
                            )]),
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
                            )]),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/cLRmBTe.jpg',
                        title='其他',
                        text='其他',
                        actions=[
                            MessageTemplateAction(
                                label='關於鮮蔬盒的介紹與起源',
                                text='關於鮮蔬盒'
                            ),
                            MessageTemplateAction(
                                label='菜單與分類',
                                text='菜單與分類'
                            ),
                            MessageTemplateAction(
                                label='刪除購物籃內所有組合商品',
                                text='刪除購物籃內所有組合商品'
                            )])
                ]))
        line_bot_api.reply_message(event.reply_token,message)
    elif event.message.text[0] == '買':
        product = event.message.text[1:]
        dic = {'username':name,
           'creattime':datetime.now(),
           'product':product}
        mongodb.insert_one(dic,'vmproduct')
        message = TextSendMessage(text='小鮮盒已經收到囉~~還要其他的嗎?')
        name_active = str(name)+':'+str(event.message.text)
        line_bot_api.push_message(os.environ['gene_uid'], TextSendMessage(text=name_active))
        line_bot_api.reply_message(event.reply_token,message)
    
    elif event.message.text[0:2] == '更改':
        if event.message.text[2:8] == '鮮蔬果大組合|鮮蔬果中組合|鮮蔬果小組合':
            product_ = event.message.text[2:8]
        elif event.message.text[2:9] == '當季蔬果大組合|當季蔬果中組合|當季蔬果小組合|綠色蔬菜大組合|綠色蔬菜中組合|綠色蔬菜小組合':
            product_ = event.message.text[2:9]
        elif event.message.text[2:7] == '烤肉大組合|烤肉中組合|烤肉小組合|拜拜大組合|拜拜中組合|拜拜小組合':
            product_ = event.message.text[2:7]
        count_change = event.message.text[-1]
        update_user_product_count(uid,'vproduct',product_,count_change)
        message = '已'+str(event.message.text[0:2]) + str(product_) + '為' + str(count_change) + '份'
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
