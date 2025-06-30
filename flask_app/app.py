from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = 'tasks.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL
            )
        ''')

@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        tasks = conn.execute('SELECT id, title FROM tasks').fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if request.method == 'POST':
        new_title = request.form['title']
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute('UPDATE tasks SET title = ? WHERE id = ?', (new_title, task_id))
        return redirect(url_for('index'))
    else:
        with sqlite3.connect(DB_NAME) as conn:
            task = conn.execute('SELECT id, title FROM tasks WHERE id = ?', (task_id,)).fetchone()
        return render_template('edit.html', task=task)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)