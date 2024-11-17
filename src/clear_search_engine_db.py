import sqlite3

def clear_database(db_name="src/search_engine.db"):
    """Clears all tables in the specified SQLite database."""
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        try:
            # List all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            # Drop each table
            for table in tables:
                print(f"Dropping table: {table[0]}")
                cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")
            
            conn.commit()
            print("Database cleared successfully.")
        except Exception as e:
            print(f"Error while clearing database: {e}")

if __name__ == "__main__":
    clear_database()
