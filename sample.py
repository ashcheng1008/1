from flask import Flask, request, abort
import os

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

# 使用heroku的environment variables
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


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
# 傳送訊息到 line
  def handle_message(event):
    # 設定回覆訊息
    message = {
        "type": "imagemap",
        "baseUrl": "https://www.google.com/maps/uv?hl=zh-TW&pb=!1s0x34682231ba47afbd%3A0xdea0c1705504bd52!2m22!2m2!1i80!2i80!3m1!2i20!16m16!1b1!2m2!1m1!1e1!2m2!1m1!1e3!2m2!1m1!1e5!2m2!1m1!1e4!2m2!1m1!1e6!3m1!7e115!4shttps%3A%2F%2Flh5.googleusercontent.com%2Fp%2FAF1QipOGS7yb2HwrJ1d0GFmpe8ReWONc5xP4ORfiXfqP%3Dw319-h320-k-no!5z5YSE6LuS5Lit6Yar6Ki65omAIC0gR29vZ2xlIOaQnOWwiw!15sCAQ&imagekey=!1e10!2sAF1QipOGS7yb2HwrJ1d0GFmpe8ReWONc5xP4ORfiXfqP&sa=X&ved=2ahUKEwiCleeS3M_jAhXJxosBHRt2CosQoiowDHoECAsQBg#",
        "altText": "億軒中醫診所1",
        "baseSize": {
            "height": 1040,
            "width": 1040
        },
        "actions": [
            {
                "type": "uri",
                "linkUri": "http://yi-hsuan.tcm.tw",
                "label": "億軒中醫診所2",
                "area": {
                    "x": 0,
                    "y": 0,
                    "width": 520,
                    "height": 1040
                }
            },
            {
                "type": "message",
                "text": "億軒中醫診所3",
                "area": {
                    "x": 520,
                    "y": 0,
                    "width": 520,
                    "height": 1040
                }
            }
        ]
    }
    # 傳送訊息
    line.reply_message(reply_token, message)
  end

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    # Setting host='0.0.0.0' will make Flask available from the network
    app.run(host='0.0.0.0', port=port)
