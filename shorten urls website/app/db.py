import sqlite3
import os

# Define the path to the database file
DATABASE = os.path.join('instance', 'url_shortener.db')

def create_database():
    # Ensure the instance folder exists
    if not os.path.exists('instance'):
        os.makedirs('instance')
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS url (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        short_code TEXT UNIQUE,
        url TEXT
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
