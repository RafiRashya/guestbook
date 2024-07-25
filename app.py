from create_db import make_db
from flask import Flask, render_template, url_for, redirect
from forms import SubmitForm
from logging import FileHandler, WARNING
from pathlib import Path
import mysql.connector as mysql

file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your secret key goes here'  # ToDo replace this with your secret key
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'rafi'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'guestbook'

app.logger.addHandler(file_handler)

def get_db_connection():
    conn = mysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    form = SubmitForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, message) VALUES (%s, %s)', (form.username.data, form.message.data))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('view'))
    return render_template('submit.html', form=form)

@app.route('/view')
def view():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, message FROM users')
    users = cursor.fetchall()  # Fetch all results from the query
    cursor.close()
    conn.close()
    return render_template('view.html', users=users)

if __name__ == '__main__':
    with app.app_context():
        make_db(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
    app.run(host='0.0.0.0', port=8080)