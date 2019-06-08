from flask import Flask, request, abort
from time import sleep

import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import requests
import json

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
AUTHORIZATION_KEY = os.environ["AUTH_KEY"]
KEYWORD = os.environ.get("KEYWORD")
ENDPOINTS = os.environ.get("ENDPOINTS").split(";")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


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
    print(event.message.text)
    if event.message.text == KEYWORD:
        _unlock_doors()
        sleep(10)
        status = _confirm_doors_status()

        if any(status):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Some of door(s) still closed")
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Opened your door(s)")
            )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Don't come in. Will alert to the police!!"))


def _unlock_doors():
    for endpoint in ENDPOINTS:
        requests.post(
            'https://api.candyhouse.co/public/sesame/' + endpoint,
            json.dumps({"command": "unlock"}),
            headers={'Content-Type': 'application/json', 'Authorization': AUTHORIZATION_KEY}
        )
        sleep(1)


def _confirm_doors_status():
    status = []
    for endpoint in ENDPOINTS:
        response = requests.get(
            'https://api.candyhouse.co/public/sesame/' + endpoint,
            headers={'Content-Type': 'application/json', 'Authorization': AUTHORIZATION_KEY}).json()
        status.append(response['locked'])
    print(status)
    return status


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
