from flask import Flask, request
from scheduler import start_scheduler
import sqlite3
import os

app = Flask(__name__)

# 🔥 Start scheduler immediately (important for Render)
start_scheduler()

@app.route("/")
def home():
    return "Medicine Reminder Agent Running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"].lower()

        if text == "yes":
            conn = sqlite3.connect("patients.db")
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE patients
                SET confirmed=1
                WHERE chat_id=?
            """, (str(chat_id),))

            conn.commit()
            conn.close()

            print(f"{chat_id} confirmed medicine.")

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))