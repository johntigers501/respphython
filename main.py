# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, TextSendMessage

load_dotenv()

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])  # URL สำหรับ webhook
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)  # รับข้อความจากผู้ใช้
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Hello, this is a response from your Line Bot!')
    )

if __name__ == '__main__':
    app.run(port=3000)
