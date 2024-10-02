from bottle import Bottle, route, static_file, template, request

app = Bottle()

# Route to serve static files (CSS, JS, images, etc.)
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./static')

@app.route('/')
def main_site():
    return template('index') 

@app.route("/search", method="POST")
def search():
    user_query = request.forms.get('query')
    words = user_query.lower().split()
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1 

    return template('result_page', user_query=user_query, word_count=word_count)
    
if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)

    
