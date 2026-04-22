from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("libros.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            genero TEXT NOT NULL,
            imagen TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

# CREATE
@app.route("/libros", methods=["POST"])
def crear():
    data = request.json
    conn = get_db()

    conn.execute(
        "INSERT INTO libros (titulo, autor, genero, imagen) VALUES (?, ?, ?, ?)",
        (data["titulo"], data["autor"], data["genero"], data["imagen"])
    )

    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Creado"})

# UPDATE
@app.route("/libros/<int:id>", methods=["PUT"])
def actualizar(id):
    data = request.json
    conn = get_db()

    libro_actual = conn.execute("SELECT * FROM libros WHERE id=?", (id,)).fetchone()
    if libro_actual is None:
        conn.close()
        return jsonify({"mensaje": "No encontrado"}), 404

    imagen = data.get("imagen") if data.get("imagen") else libro_actual["imagen"]

    conn.execute(
        """
        UPDATE libros
        SET titulo=?, autor=?, genero=?, imagen=?
        WHERE id=?
        """,
        (data["titulo"], data["autor"], data["genero"], imagen, id)
    )

    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Actualizado"})

# READ
@app.route("/libros", methods=["GET"])
def leer():
    conn = get_db()
    libros = conn.execute("SELECT * FROM libros").fetchall()
    conn.close()

    return jsonify([
        {
            "id": l["id"],
            "titulo": l["titulo"],
            "autor": l["autor"],
            "genero": l["genero"],
            "imagen": l["imagen"]
        }
        for l in libros
    ])

# DELETE
@app.route("/libros/<int:id>", methods=["DELETE"])
def eliminar(id):
    conn = get_db()
    conn.execute("DELETE FROM libros WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Eliminado"})

if __name__ == "__main__":
    app.run(debug=True)