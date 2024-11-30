from difflib import SequenceMatcher

class SpellChecker:
    def __init__(self, trie):
        self.trie = trie

    def get_suggestions(self, typo_word, max_results=1):
        """
        Find the closest word(s) in the trie for the given typo_word.
        """
        def get_similarity(word1, word2):
            return SequenceMatcher(None, word1, word2).ratio()

        all_words = self._collect_words_from_trie(self.trie.root)
        scored_words = [(word, get_similarity(typo_word, word)) for word in all_words]
        scored_words.sort(key=lambda x: x[1], reverse=True)  # Sort by similarity (highest first)
        return [word for word, score in scored_words[:max_results]]

    def _collect_words_from_trie(self, node, prefix="", words=None):
        """
        Recursively collect all words from the trie.
        """
        if words is None:
            words = []
        if node.is_end_of_word:
            words.append(prefix)
        for char, child in node.children.items():
            self._collect_words_from_trie(child, prefix + char, words)
        return words
