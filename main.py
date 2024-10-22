# -*- coding: utf-8 -*-
import os
from linebot.v3 import LineBotApi, WebhookHandler
from linebot.v3.models import MessageEvent, TextMessage, TextSendMessage
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except Exception as e:
        print(e)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)  # รับข้อความจากผู้ใช้
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)  # ส่งข้อความกลับไปยังผู้ใช้
    )

if __name__ == "__main__":
    app.run(port=3000)
