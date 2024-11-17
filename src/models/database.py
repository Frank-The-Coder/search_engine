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
    last_search_word = cursor.execute(
        '''
        SELECT search_word FROM search_history
        ORDER BY timestamp DESC
        LIMIT 1
        '''
    ).fetchone()[0]
    if search_word == last_search_word:
        return
    cursor.execute(
        'INSERT INTO search_history (email, search_word) VALUES (?, ?)',
        (email, search_word)
    )
    conn.commit()
    conn.close()


'''
Get the url list from the page
@return url_list
@return total_page
'''
def get_pages_from_search(search_word, items_per_page, page_number):

    conn = sqlite3.connect('search_engine.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS TempResults')
    cursor.execute(
        '''
        CREATE TEMPORARY TABLE TempResults AS
        SELECT DISTINCT
            PageRank.url
        FROM
            Lexicon
        JOIN
            InvertedIndex ON Lexicon.word_id = InvertedIndex.word_id
        JOIN
            DocumentIndex ON InvertedIndex.doc_id = DocumentIndex.doc_id
        JOIN
            PageRank ON DocumentIndex.url = PageRank.url
        WHERE
            Lexicon.word = ? 
        ORDER BY
            PageRank.score DESC
        ''', 
        [search_word]
    )

    total_items = cursor.execute('SELECT COUNT(*) FROM TempResults').fetchone()[0]

    total_pages = max((total_items + items_per_page - 1) // items_per_page, 1)  # Ceiling division

    # TODO: instead of setting the overflow page to last page, direct to error page instead
    if page_number < 1 or page_number > total_pages:
        raise ValueError("Page number out of bound")

    page_offset = (page_number-1) * items_per_page

    if page_offset > total_items:
        return []

    cursor.execute(
        '''
        SELECT url FROM TempResults
        LIMIT ? OFFSET ?
        ''', 
        [items_per_page, page_offset]
    )
    results = cursor.fetchall()
    conn.close()

    return [url[0] for url in results], total_pages
