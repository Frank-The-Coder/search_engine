import sqlite3

def get_recent_searches(email):
    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT search_word, timestamp FROM search_history WHERE email = ? ORDER BY timestamp DESC LIMIT 10',
        (email,)
    )
    results = cursor.fetchall()
    conn.close()
    return results

def save_search(email, search_word):
    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO search_history (email, search_word) VALUES (?, ?)',
        (email, search_word)
    )
    conn.commit()
    conn.close()
