from flask import Flask, request, render_template_string
import sqlite3
import hashlib
import os
from datetime import datetime

app = Flask(__name__)

DATABASE = "database.db"
UPLOAD_FOLDER = "cloud_storage"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

duplicate_count = 0

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        filehash TEXT UNIQUE,
        upload_date TEXT
    )
    """)

    conn.commit()
    conn.close()

def get_file_hash(file):
    sha256 = hashlib.sha256()

    while True:
        chunk = file.read(4096)
        if not chunk:
            break
        sha256.update(chunk)

    file.seek(0)
    return sha256.hexdigest()

init_db()

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Data Redundancy Removal System</title>

<style>
body{
    font-family:Arial,sans-serif;
    background:#f4f6f9;
    padding:30px;
}

.container{
    max-width:1000px;
    margin:auto;
    background:white;
    padding:25px;
    border-radius:10px;
    box-shadow:0px 0px 10px rgba(0,0,0,0.15);
}

h1{
    text-align:center;
    color:#333;
}

.stats{
    display:flex;
    gap:20px;
    margin-bottom:20px;
}

.card{
    flex:1;
    background:#e8f0fe;
    border-radius:8px;
    padding:15px;
    text-align:center;
}

.card h2{
    margin:0;
}

form{
    text-align:center;
    margin:20px 0;
}

button{
    padding:10px 20px;
    cursor:pointer;
}

.success{
    color:green;
    font-weight:bold;
    text-align:center;
}

.error{
    color:red;
    font-weight:bold;
    text-align:center;
}

table{
    width:100%;
    border-collapse:collapse;
    margin-top:20px;
}

th,td{
    border:1px solid #ddd;
    padding:10px;
    text-align:center;
}

th{
    background:#0078d7;
    color:white;
}
</style>

</head>

<body>

<div class="container">

<h1>Data Redundancy Removal System</h1>

<div class="stats">

<div class="card">
<h3>Total Unique Files</h3>
<h2>{{total}}</h2>
</div>

<div class="card">
<h3>Duplicates Blocked</h3>
<h2>{{duplicates}}</h2>
</div>

</div>

<form method="POST" enctype="multipart/form-data">
<input type="file" name="file" required>
<button type="submit">Upload</button>
</form>

<p class="{{msg_class}}">
{{message}}
</p>

<h2>Upload History</h2>

<table>
<tr>
<th>ID</th>
<th>Filename</th>
<th>Upload Date</th>
</tr>

{% for row in rows %}
<tr>
<td>{{row[0]}}</td>
<td>{{row[1]}}</td>
<td>{{row[3]}}</td>
</tr>
{% endfor %}

</table>

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    global duplicate_count

    message = ""
    msg_class = ""

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if request.method == "POST":

        file = request.files["file"]

        if file:

            file_hash = get_file_hash(file)

            cursor.execute(
                "SELECT * FROM files WHERE filehash=?",
                (file_hash,)
            )

            existing = cursor.fetchone()

            if existing:

                duplicate_count += 1

                message = "Duplicate File Detected! Storage Prevented."
                msg_class = "error"

            else:

                filepath = os.path.join(
                    UPLOAD_FOLDER,
                    file.filename
                )

                file.save(filepath)

                upload_date = datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                )

                cursor.execute(
                    """
                    INSERT INTO files
                    (filename,filehash,upload_date)
                    VALUES (?,?,?)
                    """,
                    (
                        file.filename,
                        file_hash,
                        upload_date
                    )
                )

                conn.commit()

                message = "Unique File Stored Successfully."
                msg_class = "success"

    cursor.execute(
        "SELECT * FROM files ORDER BY id DESC"
    )

    rows = cursor.fetchall()

    cursor.execute(
        "SELECT COUNT(*) FROM files"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return render_template_string(
        HTML,
        rows=rows,
        total=total,
        duplicates=duplicate_count,
        message=message,
        msg_class=msg_class
    )

if __name__ == "__main__":
    app.run(debug=True)