import sqlite3

DATABASE = 'voting.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create voters table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS voters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            photo_path TEXT,
            voted INTEGER DEFAULT 0
        )
    ''')
    # Create votes table (optional for redundancy)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_id INTEGER,
            candidate TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def register_voter(name, photo_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO voters (name, photo_path) VALUES (?, ?)", (name, photo_path))
    conn.commit()
    conn.close()

def get_voter_photo(voter_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT photo_path FROM voters WHERE id = ?", (voter_id,))
    row = cursor.fetchone()
    conn.close()
    return row['photo_path'] if row else None

def has_voted(voter_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT voted FROM voters WHERE id = ?", (voter_id,))
    row = cursor.fetchone()
    conn.close()
    return row['voted'] == 1 if row else False

def mark_voted(voter_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE voters SET voted = 1 WHERE id = ?", (voter_id,))
    conn.commit()
    conn.close()

def store_vote(voter_id, candidate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO votes (voter_id, candidate) VALUES (?, ?)", (voter_id, candidate))
    conn.commit()
    conn.close()
