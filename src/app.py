from bottle import Bottle, run, static_file
from beaker.middleware import SessionMiddleware
from routes.auth import auth_routes
from routes.search import search_routes
from routes.home import home_routes
from routes.error import register_error_handlers
from config import IS_DEPLOY

# Initialize the Bottle app
app = Bottle()

# Serve static files (e.g., CSS, JS)
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    """Serve static files from the 'static' directory."""
    return static_file(filepath, root='./static')

# Session middleware configuration
session_opts = {
    'session.type': 'memory',
    'session.auto': True,
    'session.cookie_expires': 86400,
    'session.timeout': 86400,
    'session.lock_dir': './session_locks'
}
app_with_sessions = SessionMiddleware(app, session_opts)

# Register route modules
app.merge(auth_routes)
app.merge(search_routes)
app.merge(home_routes)

# Register error handlers
register_error_handlers(app)

# Run the app
if __name__ == "__main__":
    APP_PORT = 8080
    HOST_NAME = '0.0.0.0'

    if IS_DEPLOY:
        APP_PORT = 80
        HOST_NAME = '0.0.0.0'

    run(app=app_with_sessions, host=HOST_NAME, port=APP_PORT, debug=True)
