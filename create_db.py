import sqlite3
from werkzeug.security import generate_password_hash

# Connect to SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create test users (with hashed passwords)
test_users = [
    ('john_doe', 'password123'),
    ('jane_doe', 'securepass456'),
    ('admin', 'adminpassword789')
]

# Insert test data into the users table
for username, password in test_users:
    # Use pbkdf2:sha256 for password hashing
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))

# Commit and close the connection
conn.commit()
conn.close()

print("Test data inserted successfully.")
