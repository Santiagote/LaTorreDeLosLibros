from flask import Flask, request, jsonify, render_template
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)

def get_db():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            genero TEXT NOT NULL,
            imagen TEXT
        )
    """)
    conn.commit()
    cur.close()
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
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO libros (titulo, autor, genero, imagen) VALUES (%s, %s, %s, %s)",
        (data["titulo"], data["autor"], data["genero"], data["imagen"])
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Creado"})

# READ
@app.route("/libros", methods=["GET"])
def leer():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM libros")
    libros = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(list(libros))

# UPDATE
@app.route("/libros/<int:id>", methods=["PUT"])
def actualizar(id):
    data = request.json
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM libros WHERE id=%s", (id,))
    libro_actual = cur.fetchone()
    if libro_actual is None:
        cur.close()
        conn.close()
        return jsonify({"mensaje": "No encontrado"}), 404
    imagen = data.get("imagen") if data.get("imagen") else libro_actual["imagen"]
    cur.execute(
        "UPDATE libros SET titulo=%s, autor=%s, genero=%s, imagen=%s WHERE id=%s",
        (data["titulo"], data["autor"], data["genero"], imagen, id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Actualizado"})

# DELETE
@app.route("/libros/<int:id>", methods=["DELETE"])
def eliminar(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM libros WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Eliminado"})

if __name__ == "__main__":
    app.run(debug=True)