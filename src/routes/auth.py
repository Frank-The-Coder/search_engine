from bottle import Bottle, redirect, request, response
from utils.oauth import handle_oauth_redirect
from oauth2client.client import flow_from_clientsecrets
from config import MAIN_URL

auth_routes = Bottle()

CLIENT_SECRET_FILE = "client_secret.json"
REDIRECT_URI = MAIN_URL + "/redirect"
SCOPES = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

@auth_routes.route('/login')
def login():
    flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.redirect_uri = REDIRECT_URI
    auth_uri = flow.step1_get_authorize_url()
    return redirect(auth_uri)

@auth_routes.route('/redirect')
def oauth_redirect():
    return handle_oauth_redirect()

@auth_routes.route('/signout', method='POST')
def signout():
    session = request.environ.get('beaker.session')
    session.delete()
    response.status = 200
    return "Logged out successfully"
