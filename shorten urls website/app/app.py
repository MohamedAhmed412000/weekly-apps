from flask import Flask, request, redirect, render_template
import sqlite3
import random
import string
import os

app = Flask(__name__)

# Define the path to the database file
DATABASE = os.path.join(app.instance_path, 'url_shortener.db')

# Generate a short code for the URL
def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# Function to get a database connection
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Function to check if a URL already has a short code in the database
def get_existing_short_code(url):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT short_code FROM url WHERE url = ?', (url,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row['short_code']
    return None

# Function to save the URL and short code to the database
def save_url(url):
    short_code = get_existing_short_code(url)
    if short_code is None:
        short_code = generate_short_code()
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO url (short_code, url) VALUES (?, ?)', (short_code, url))
        conn.commit()
        conn.close()
    return short_code

# Function to retrieve the original URL from the database using the short code
def get_url(short_code):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT url FROM url WHERE short_code = ?', (short_code,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row['url']
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        short_code = save_url(original_url)
        return render_template('index.html', short_code=short_code, original_url=original_url)
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    original_url = get_url(short_code)
    if original_url:
        return redirect(original_url)
    return 'URL not found', 404

if __name__ == '__main__':
    # Ensure the instance folder exists
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
    app.run(debug=True)
