import sqlite3

def init_db():
    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()

    # Create table for search history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_history (
            email TEXT NOT NULL,
            search_word TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
