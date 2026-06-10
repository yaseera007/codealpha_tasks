from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from cryptography.fernet import Fernet
from datetime import datetime

app = Flask(__name__)
app.secret_key = "CODEALPHA_SECRET_KEY"

DATABASE = "users.db"
KEY_FILE = "secret.key"
CAPABILITY_CODE = "CODEALPHA2026"

# -------------------------------
# Encryption Key Setup
# -------------------------------

if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, "wb") as f:
        f.write(Fernet.generate_key())

with open(KEY_FILE, "rb") as f:
    key = f.read()

cipher = Fernet(key)

# -------------------------------
# Database Setup
# -------------------------------

def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS security_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# -------------------------------
# Security Logging
# -------------------------------

def log_event(event):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO security_logs(event,timestamp) VALUES(?,?)",
        (
            event,
            datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        )
    )

    conn.commit()
    conn.close()

# -------------------------------
# SQL Injection Detection
# -------------------------------

def detect_sql_injection(text):

    patterns = [
        "' OR",
        '" OR',
        "--",
        ";",
        "DROP",
        "DELETE",
        "UNION",
        "SELECT *",
        "1=1",
        "INSERT INTO"
    ]

    text = text.upper()

    for pattern in patterns:
        if pattern.upper() in text:
            return True

    return False

# -------------------------------
# Home
# -------------------------------

@app.route("/")
def home():
    return redirect("/login")

# -------------------------------
# Register
# -------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        capability = request.form["capability"]

        # Capability Code Validation

        if capability != CAPABILITY_CODE:

            message = "Invalid Capability Code"

            log_event(
                "Blocked Registration - Invalid Capability Code"
            )

            return render_template(
                "register.html",
                message=message
            )

        # SQL Injection Detection

        if detect_sql_injection(username) or detect_sql_injection(password):

            message = "SQL Injection Attempt Detected"

            log_event(
                "Blocked SQL Injection During Registration"
            )

            return render_template(
                "register.html",
                message=message
            )

        encrypted_password = cipher.encrypt(
            password.encode()
        ).decode()

        try:

            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()

            cur.execute(
                """
                INSERT INTO users
                (username,password,created_at)
                VALUES(?,?,?)
                """,
                (
                    username,
                    encrypted_password,
                    datetime.now().strftime(
                        "%d-%m-%Y %H:%M:%S"
                    )
                )
            )

            conn.commit()
            conn.close()

            log_event(
                f"New User Registered : {username}"
            )

            message = "Registration Successful"

        except:

            message = "Username Already Exists"

    return render_template(
        "register.html",
        message=message
    )

# -------------------------------
# Login
# -------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if detect_sql_injection(username) or detect_sql_injection(password):

            message = "SQL Injection Attempt Blocked"

            log_event(
                "Blocked SQL Injection During Login"
            )

            return render_template(
                "login.html",
                message=message
            )

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()

        cur.execute(
            """
            SELECT password
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        user = cur.fetchone()

        conn.close()

        if user:

            decrypted_password = cipher.decrypt(
                user[0].encode()
            ).decode()

            if password == decrypted_password:

                session["user"] = username

                log_event(
                    f"Successful Login : {username}"
                )

                return redirect("/dashboard")

        message = "Invalid Username or Password"

        log_event(
            "Failed Login Attempt"
        )

    return render_template(
        "login.html",
        message=message
    )

# -------------------------------
# Dashboard
# -------------------------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM users"
    )

    total_users = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM security_logs"
    )

    total_logs = cur.fetchone()[0]

    cur.execute(
        """
        SELECT *
        FROM security_logs
        ORDER BY id DESC
        LIMIT 10
        """
    )

    logs = cur.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        username=session["user"],
        total_users=total_users,
        total_logs=total_logs,
        logs=logs
    )

# -------------------------------
# Logout
# -------------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

# -------------------------------
# Run
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)