from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "peers.db"

# ----- Database setup -----
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS peers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ----- Routes -----
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    ip = data.get("ip")
    if not ip:
        return jsonify({"error": "No IP provided"}), 400

    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO peers (ip) VALUES (?)", (ip,))
        conn.commit()
        conn.close()
        return jsonify({"message": f"IP {ip} registered successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/peers", methods=["GET"])
def get_peers():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT ip FROM peers")
    rows = c.fetchall()
    conn.close()
    return jsonify({"peers": [row[0] for row in rows]})
