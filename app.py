import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = "8336549556:AAFcMSnakNYWbUGgPRMNV4E2k91GIfyupjQ"
CHAT_ID = "3089784234"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    text = f"OpenAI Event: {data}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    return '', 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
