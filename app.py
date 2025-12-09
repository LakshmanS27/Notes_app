from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

#Database
def init_db():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

#HTML Routes
@app.route("/")
def home():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    rows = c.fetchall()
    conn.close()
    return render_template("index.html", notes=rows)

@app.route("/add", methods=["POST"])
def add_note():
    content = request.form.get("content")
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("INSERT INTO notes (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete_note(id):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

#PI Routes
@app.route("/api/notes", methods=["GET"])
def api_get_notes():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("SELECT id, content FROM notes")
    rows = c.fetchall()
    conn.close()
    notes = [{"id": r[0], "content": r[1]} for r in rows]
    return jsonify(notes)

@app.route("/api/notes", methods=["POST"])
def api_add_note():
    data = request.get_json()
    content = data.get("content")
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("INSERT INTO notes (content) VALUES (?)", (content,))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return jsonify({"id": new_id, "content": content}), 201

@app.route("/api/notes/<int:id>", methods=["DELETE"])
def api_delete_note(id):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"id": id, "message": "Deleted"})


if __name__ == "__main__":
    app.run(debug=True)