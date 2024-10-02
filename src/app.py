from bottle import Bottle, route, static_file, template 

app = Bottle()

# Route to serve static files (CSS, JS, images, etc.)
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./static')

@app.route('/')
def main_site():
    return template('index') 

if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)

    
