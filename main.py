from flask import Flask, request
import anthropic
import requests
import os

app = Flask(__name__)

LINE_TOKEN = os.environ.get("LINE_TOKEN")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_KEY")

claude = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.json
    for event in body.get("events", []):
        if event["type"] == "message" and event["message"]["type"] == "text":
            user_message = event["message"]["text"]
            reply_token = event["replyToken"]

            response = claude.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                messages=[{"role": "user", "content": user_message}]
            )
            reply_text = response.content[0].text

            requests.post(
                "https://api.line.me/v2/bot/message/reply",
                headers={"Authorization": f"Bearer {LINE_TOKEN}"},
                json={"replyToken": reply_token, "messages": [{"type": "text", "text": reply_text}]}
            )
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
