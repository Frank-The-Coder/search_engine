from bottle import Bottle, route, static_file, template, request
from heapq import heapify, heappop, heappush, heappushpop

class SearchHistory:
# Store how many times each keyword have been searched, and the top 20 occurance
    def __init__(self):
        self.count_dict = {}
        self.top_20_list = []

    def insert(self, word, count):
        assert len(self.top_20_list) <=20

        if word in self.count_dict:
            self.count_dict[word] += count
        else:
            self.count_dict[word] = count

        for i, (_, top_word) in enumerate(self.top_20_list):
            if word == top_word:
                self.top_20_list[i] = (self.count_dict[word], word)
                self.top_20_list = sorted(self.top_20_list, key = lambda x: x[0], reverse=True)
                return

        if len(self.top_20_list) < 20:
            self.top_20_list.append((count, word))

        elif self.top_20_list[19][0] < self.count_dict[word]:
            self.top_20_list[19] = (self.count_dict[word], word)
            
        self.top_20_list = sorted(self.top_20_list, key = lambda x: x[0], reverse=True)

    def get_top_20(self):
        return self.top_20_list
 
app = Bottle()
search_history = SearchHistory()
     

# Route to serve static files (CSS, JS, images, etc.)
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./static')

@app.route('/')
def main_site():
    return template('index', top_20_list=search_history.get_top_20()) 

@app.route("/search", method="POST")
def search():
    user_query = request.forms.get('keywords')
    words = user_query.lower().split()
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1

    for key, val in word_count.items():
        search_history.insert(key, val)
    print(search_history.get_top_20())

    return template('result_page', user_query=user_query, word_count=word_count)
    
if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)

    
