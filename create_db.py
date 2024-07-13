import mysql.connector as mysql

def make_db(host, user, password, database):
    conn = mysql.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {database}')
    cursor.execute(f'USE {database}')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            message TEXT
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()
