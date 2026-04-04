from flask import Flask, jsonify, request
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB_NAME = os.environ.get("DB_NAME", "aceest.db")

PROGRAMS = {
    "Fat Loss (FL)": {"calorie_factor": 22},
    "Muscle Gain (MG)": {"calorie_factor": 35},
    "Beginner (BG)": {"calorie_factor": 26},
}


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            age INTEGER,
            weight REAL,
            program TEXT,
            calories INTEGER,
            created_at TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            week TEXT,
            adherence INTEGER
        )
    """)
    conn.commit()
    conn.close()


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def calculate_calories(weight, program):
    factor = PROGRAMS.get(program, {}).get("calorie_factor", 26)
    return int(weight * factor)


@app.route("/")
def index():
    return jsonify({
        "app": "ACEest Fitness & Gym",
        "version": "3.2.4",
        "status": "running",
        "programs": list(PROGRAMS.keys())
    }), 200


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/programs", methods=["GET"])
def get_programs():
    return jsonify({"programs": list(PROGRAMS.keys())}), 200


@app.route("/programs/<program_name>", methods=["GET"])
def get_program(program_name):
    matched = next(
        (k for k in PROGRAMS
         if k.lower().replace(" ", "-") ==
         program_name.lower().replace(" ", "-")),
        None
    )
    if not matched:
        return jsonify({"error": "Program not found"}), 404
    return jsonify({"program": matched, "details": PROGRAMS[matched]}), 200


@app.route("/clients", methods=["GET"])
def get_clients():
    conn = get_db()
    rows = conn.execute("SELECT * FROM clients ORDER BY name").fetchall()
    conn.close()
    return jsonify({"clients": [dict(r) for r in rows]}), 200


@app.route("/clients", methods=["POST"])
def add_client():
    data = request.get_json()
    name = data.get("name", "").strip()
    age = data.get("age", 0)
    weight = data.get("weight", 0.0)
    program = data.get("program", "")

    if not name:
        return jsonify({"error": "Name is required"}), 400
    if program not in PROGRAMS:
        return jsonify({"error": "Invalid program"}), 400
    if weight <= 0:
        return jsonify({"error": "Weight must be > 0"}), 400

    calories = calculate_calories(weight, program)
    conn = get_db()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO clients "
            "(name, age, weight, program, calories, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (name, age, weight, program, calories,
             datetime.now().isoformat())
        )
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500
    conn.close()
    return jsonify({
        "message": f"Client '{name}' saved",
        "calories": calories
    }), 201


@app.route("/clients/<name>", methods=["GET"])
def get_client(name):
    conn = get_db()
    client = conn.execute(
        "SELECT * FROM clients WHERE LOWER(name) = LOWER(?)",
        (name,)
    ).fetchone()
    conn.close()
    if not client:
        return jsonify({"error": "Client not found"}), 404
    return jsonify({"client": dict(client)}), 200


@app.route("/clients/<name>/progress", methods=["POST"])
def log_progress(name):
    data = request.get_json()
    adherence = data.get("adherence", 0)
    week = datetime.now().strftime("Week %U - %Y")
    conn = get_db()
    conn.execute(
        "INSERT INTO progress (client_name, week, adherence) "
        "VALUES (?, ?, ?)",
        (name, week, adherence)
    )
    conn.commit()
    conn.close()
    return jsonify({
        "message": "Progress logged",
        "week": week,
        "adherence": adherence
    }), 201


@app.route("/clients/<name>/progress", methods=["GET"])
def get_progress(name):
    conn = get_db()
    rows = conn.execute(
        "SELECT week, adherence FROM progress "
        "WHERE client_name = ? ORDER BY id",
        (name,)
    ).fetchall()
    conn.close()
    return jsonify({
        "client": name,
        "progress": [dict(r) for r in rows]
    }), 200


@app.route("/calories", methods=["GET"])
def estimate_calories():
    weight = request.args.get("weight", type=float)
    program = request.args.get("program", type=str)
    if not weight or not program:
        return jsonify({"error": "Provide weight and program"}), 400
    if program not in PROGRAMS:
        return jsonify({"error": "Unknown program"}), 400
    return jsonify({
        "weight": weight,
        "program": program,
        "calories": calculate_calories(weight, program)
    }), 200


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
