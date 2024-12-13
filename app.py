from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai
import os


line_bot_api = LineBotApi(os.environ.get('LineBotApi'))
handler = WebhookHandler(os.environ.get('Webhookhandler'))
genai.configure(api_key=os.environ.get('api_key'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userText = event.message.text
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(userText)
    response_data = response.text
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response_data))

if __name__ == '__main__':
    app.run(debug=True)
