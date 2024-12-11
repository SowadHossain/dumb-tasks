from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # Allows for access to columns by name
    return conn

# Home route (index page)
@app.route('/')
def home():
    return render_template('login.html')

# Route for registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = c.fetchone()

        if existing_user:
            conn.close()
            # You can pass an error message to the template if the username exists
            return render_template('register.html', error="Username already exists, please choose another one.")
        
        # Hash the password using a more secure method
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Insert new user into the database
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()

        # Redirect to the login page after successful registration
        return redirect(url_for('home'))  

    return render_template('register.html')

# Route for login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Connect to DB and check if user exists
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()

    # Check if user exists and if the password matches the hashed one in the DB
    if user and check_password_hash(user['password'], password):
        return redirect(url_for('welcome', username=username))
    else:
        return render_template('login.html', error="Invalid username or password, please try again.")

# Welcome route after successful login
@app.route('/welcome/<username>')
def welcome(username):
    return f"Welcome {username}!"

if __name__ == '__main__':
    app.run(debug=True)
