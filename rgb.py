from create_db import make_db
from flask import Flask, render_template, url_for, redirect
from forms import SubmitForm
from pathlib import Path
import sqlite3 as sql

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your secret key goes here' #ToDo replace this with your secret key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    form = SubmitForm()
    if form.validate_on_submit():
        conn = sql.connect('database.db')
        conn.execute('INSERT INTO users (username, message) VALUES (?,?)', (form.username.data, form.message.data))
        conn.commit()
        conn.close()
        return(redirect(url_for('view')))
    return render_template('submit.html', form=form)

@app.route('/view')
def view():
    conn = sql.connect('database.db')
    cursor = conn.execute('SELECT username, message from users')
    return render_template('view.html', cursor=cursor)

if __name__ == '__main__':
    if not Path('database.db').is_file():
        make_db()
    app.run(debug=True, host='0.0.0.0')

