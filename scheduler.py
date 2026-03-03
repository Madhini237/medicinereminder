from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import sqlite3
import requests

TOKEN = "7989386136:AAG-G_cbf8MSZ3lJ0P6uyuOX7Y-NILcRDe4"   # 🔴 Replace with your token


def send_message(chat_id, message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(url, data={"chat_id": chat_id, "text": message})
    print("Telegram response:", response.text)  # helpful for debugging


def check_medicines():
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    print("Checking at:", current_time)

    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()

    # ✅ Send reminder if:
    # - time matches
    # - and reminder not already sent today
    cursor.execute("""
        SELECT id, name, chat_id, medicine
        FROM patients
        WHERE time=? 
        AND (last_sent IS NULL OR DATE(last_sent) != ?)
    """, (current_time, now.date().isoformat()))

    patients = cursor.fetchall()
    print("Patients found:", patients)

    for p in patients:
        msg = f"Hi {p[1]}, please take your {p[3]}. Reply YES after taking."
        send_message(p[2], msg)

        # Store full datetime (important fix)
        cursor.execute("""
            UPDATE patients
            SET last_sent=?, confirmed=0
            WHERE id=?
        """, (now.isoformat(), p[0]))

        print(f"Reminder sent to {p[1]}")

    # ✅ Escalation logic (after 15 minutes if not confirmed)
    cursor.execute("""
        SELECT id, name, emergency_chat_id, last_sent
        FROM patients
        WHERE confirmed=0 AND last_sent IS NOT NULL
    """)

    rows = cursor.fetchall()

    for row in rows:
        sent_time = datetime.fromisoformat(row[3])

        if now - sent_time > timedelta(minutes=1):
            alert = f"{row[1]} has NOT confirmed medicine."
            send_message(row[2], alert)

            cursor.execute("""
                UPDATE patients
                SET confirmed=1
                WHERE id=?
            """, (row[0],))

            print(f"Escalation sent for {row[1]}")

    conn.commit()
    conn.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_medicines, "interval", minutes=1)
    scheduler.start()