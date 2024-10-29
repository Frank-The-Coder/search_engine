from bottle import Bottle, request, template
from models.database import save_search
from utils.oauth import get_user_info

search_routes = Bottle()

@search_routes.route('/search', method='POST')
def search():
    session = request.environ.get('beaker.session')
    user_info = get_user_info(session)

    user_query = request.forms.get('keywords', '').strip()
    word_count = {word: user_query.lower().split().count(word) for word in set(user_query.split())}

    if user_info['signedin']:
        for word in word_count:
            save_search(user_info['user_email'], word)

    return template('result_page', user_query=user_query, word_count=word_count, **user_info)
