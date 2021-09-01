from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('UZoznnOWYhmBLi8AzdReRDnfO7OerlYS2U6T34fmfF7cHx7rNpe70Le51x9TY1WQqd2gZ3/Qfr/etEZV/GdcySgB20PfyLuUbRpRfS2THDCfp9rk1WALGCOhxPhHhnHqVIc1P3xSoxs57ZQvf/5dxAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6be3793e52737e5b281e79b598764f26')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    reply = '對不起！我不知道你在說什麼'

    if msg == 'hi':
        reply = 'hello'
    elif msg == '你吃飯了嗎':
        reply = '機器人不用吃飯'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))


if __name__ == "__main__":
    app.run()