
import sqlite3
from custom_lib.crawler import crawler


class EnhancedCrawler(crawler):
    def __init__(self, db_conn, url_file):
        super().__init__(db_conn, url_file)

    def store_in_persistent_storage(self, db_name="src\search_engine.db"):
        """Store PageRank scores, lexicon, and indices in SQLite."""
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()

            # Create tables
            cursor.execute("CREATE TABLE IF NOT EXISTS PageRank (url TEXT PRIMARY KEY, score REAL);")
            cursor.execute("CREATE TABLE IF NOT EXISTS Lexicon (word TEXT PRIMARY KEY, word_id INTEGER);")
            cursor.execute("CREATE TABLE IF NOT EXISTS DocumentIndex (doc_id INTEGER PRIMARY KEY, url TEXT);")
            cursor.execute("CREATE TABLE IF NOT EXISTS InvertedIndex (word_id INTEGER, doc_id INTEGER);")

            # Store PageRank scores
            for url, score in self.compute_pagerank().items():
                cursor.execute("INSERT OR REPLACE INTO PageRank (url, score) VALUES (?, ?);", (url, score))
            # Store document index
            for url, doc_id in self._doc_id_cache.items():
                cursor.execute("INSERT OR REPLACE INTO DocumentIndex (doc_id, url) VALUES (?, ?);", (doc_id, url))

            # Store lexicon and inverted index
            for word, word_id in self._word_id_cache.items():
                cursor.execute("INSERT OR REPLACE INTO Lexicon (word, word_id) VALUES (?, ?);", (word, word_id))
            for word_id, doc_ids in self._inverted_index.items():
                for doc_id in doc_ids:
                    cursor.execute("INSERT OR REPLACE INTO InvertedIndex (word_id, doc_id) VALUES (?, ?);", (word_id, doc_id))

            conn.commit()

    def compute_pagerank(self, damping_factor=0.85, max_iterations=100, tolerance=1e-6):
        """Compute PageRank scores using link relationships."""
        urls = list(self.page_links.keys())
        num_pages = len(urls)
        scores = {url: 1 / num_pages for url in urls}

        for i in range(max_iterations):
            new_scores = {}
            for url in urls:
                incoming_links = [link for link, targets in self.page_links.items() if url in targets]
                rank_sum = sum(scores[link] / len(self.page_links[link]) for link in incoming_links)
                new_scores[url] = (1 - damping_factor) / num_pages + damping_factor * rank_sum

            # Check for convergence
            if all(abs(new_scores[url] - scores[url]) < tolerance for url in urls):
                break

            scores = new_scores

        return scores

if __name__ == "__main__":
    crawler_instance = EnhancedCrawler(None, "custom_lib/urls.txt")
    
    print("Starting crawl...")
    crawler_instance.crawl(depth=1)
    
    print("Computing PageRank...")
    crawler_instance.store_in_persistent_storage()
    print("Crawling and database generation complete.")
