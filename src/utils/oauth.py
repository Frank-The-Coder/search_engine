from oauth2client.client import flow_from_clientsecrets, OAuth2Credentials, FlowExchangeError
from googleapiclient.discovery import build
import httplib2
from bottle import request, redirect
import warnings
from config import MAIN_URL 

# Constants for OAuth
CLIENT_SECRET_FILE = "client_secret.json"
REDIRECT_URI = MAIN_URL + "redirect"
SCOPES = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

def get_user_info(session):
    """Retrieve user information using OAuth2 credentials."""
    credentials_data = session.get('credentials')
    if credentials_data:
        credentials = OAuth2Credentials.from_json(credentials_data)

        if credentials.access_token_expired:
            credentials.refresh(httplib2.Http())
            session['credentials'] = credentials.to_json()
            session.save()

        http = credentials.authorize(httplib2.Http())
        service = build('oauth2', 'v2', http=http)
        user_info = service.userinfo().get().execute()

        return {
            'signedin': True,
            'user_name': user_info.get('name', 'Anonymous User'),
            'user_email': user_info.get('email', 'No Email Provided'),
            'user_picture': user_info.get('picture', '/static/default_profile.png')
        }

    return {'signedin': False, 'user_name': None, 'user_email': None, 'user_picture': None}

def handle_oauth_redirect():
    warnings.simplefilter("ignore", ResourceWarning)

    session = request.environ.get('beaker.session')

    if request.query.get('error') == 'access_denied':
        return redirect('/')

    code = request.query.get('code')
    if not code:
        return redirect('/')

    try:
        flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=SCOPES)
        flow.redirect_uri = REDIRECT_URI

        credentials = flow.step2_exchange(code)

        session['credentials'] = credentials.to_json()
        session.save()

        http = httplib2.Http()
        http = credentials.authorize(http)

        try:
            service = build('oauth2', 'v2', http=http)
            user_info = service.userinfo().get().execute()

            session['user_info'] = {
                'name': user_info.get('name', 'Anonymous User'),
                'email': user_info.get('email', 'No Email Provided'),
                'picture': user_info.get('picture', '/static/default_profile.png')
            }
            session.save()

        finally:
            http.connections.clear()
            del http  

    except FlowExchangeError as e:
        print(f"FlowExchangeError: {e}")
        return "Authentication failed. Please try again."

    return redirect('/')
