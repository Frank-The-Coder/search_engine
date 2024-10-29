from bottle import Bottle, template, request
from models.database import get_recent_searches
from utils.oauth import get_user_info

home_routes = Bottle()

@home_routes.route('/')
def home():
    session = request.environ.get('beaker.session')
    user_info = get_user_info(session)

    if user_info['signedin']:
        recent_searches = get_recent_searches(user_info['user_email'])
    else:
        recent_searches = []

    return template('index', recent_searches=recent_searches, **user_info)
