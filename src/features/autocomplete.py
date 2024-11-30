import sqlite3
from features.spellcheck import SpellChecker

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._collect_words(node, prefix, max_results=8)  # Limit to top 8 suggestions

    def _collect_words(self, node, prefix, max_results, results=None):
        if results is None:
            results = []

        if node.is_end_of_word:
            results.append(prefix)
        if len(results) >= max_results:  # Stop collecting if limit is reached
            return results

        for char, child in node.children.items():
            results = self._collect_words(child, prefix + char, max_results, results)
            if len(results) >= max_results:  # Stop recursion early if limit is reached
                break
        return results

trie = Trie()

def initialize_trie(word_list):
    for word in word_list:
        trie.insert(word)

def get_autocomplete_suggestions(query):
    return trie.search_prefix(query.lower())


def populate_trie_from_db(db_name="search_engine.db"):
    """Populate the trie with words from the Lexicon table in the database."""
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT word FROM Lexicon;")
        words = [row[0] for row in cursor.fetchall()]  # Extract all words
        for word in words:
            trie.insert(word)  # Add each word to the trie
    
# Initialize the SpellChecker with the trie
spell_checker = SpellChecker(trie)

def get_spellcheck_suggestion(typo_word, max_results=1):
    """Get the closest matching words for a typo."""
    return spell_checker.get_suggestions(typo_word, max_results)
  