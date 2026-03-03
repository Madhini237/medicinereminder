import sqlite3

conn = sqlite3.connect("patients.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    chat_id TEXT,
    medicine TEXT,
    time TEXT,
    emergency_chat_id TEXT,
    last_sent TEXT,
    confirmed INTEGER DEFAULT 0
)
""")

# Add sample patient (CHANGE TIME BEFORE TESTING)
cursor.execute("""
INSERT INTO patients (name, chat_id, medicine, time, emergency_chat_id)
VALUES ('Ravi', '8395898873', 'BP Tablet', '23:12', '8395898873')
""")

conn.commit()
conn.close()

print("Database created successfully.")