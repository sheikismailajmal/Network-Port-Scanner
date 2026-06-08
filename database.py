import sqlite3


def create_database():
    conn = sqlite3.connect("scans.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scan_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target_ip TEXT NOT NULL,
        port INTEGER NOT NULL,
        service TEXT,
        status TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_scan_result(target_ip, port, service, status, timestamp):
    conn = sqlite3.connect("scans.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO scan_logs
        (target_ip, port, service, status, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """,
        (target_ip, port, service, status, timestamp)
    )

    conn.commit()
    conn.close()
def get_scan_history():

    conn = sqlite3.connect("scans.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM scan_logs
    ORDER BY id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records