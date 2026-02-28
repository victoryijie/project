from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "recipes.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db()
    recipes = conn.execute("SELECT * FROM recipes").fetchall()
    conn.close()
    return render_template('index.html', recipes=recipes)


@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        conn = get_db()
        conn.execute(
            "INSERT INTO recipes (title, description) VALUES (?, ?)",
            (title, description)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_recipe(id):
    conn = get_db()
    recipe = conn.execute(
        "SELECT * FROM recipes WHERE id = ?", (id,)
    ).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        conn.execute(
            "UPDATE recipes SET title=?, description=? WHERE id=?",
            (title, description, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', recipe=recipe)


@app.route('/delete/<int:id>')
def delete_recipe(id):
    conn = get_db()
    conn.execute("DELETE FROM recipes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


def init_db():
    if not os.path.exists(DB_NAME):
        conn = get_db()
        conn.execute("""
            CREATE TABLE recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
