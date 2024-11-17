from bottle import Bottle, request, template, abort
from models.database import get_pages_from_search, save_search
from utils.oauth import get_user_info

search_routes = Bottle()

@search_routes.route('/search', method='GET')
def search():
    session = request.environ.get('beaker.session')
    user_info = get_user_info(session)

    user_query = request.query.get('keywords', '').strip()
    word_count = {word: user_query.lower().split().count(word) for word in set(user_query.split())}
    
    page = int(request.query.get('page', '1'))

    if user_info['signedin']:
        for word in word_count:
            save_search(user_info['user_email'], word)

    try:
        url_results, total_pages = get_pages_from_search(user_query.lower().split()[0], 5, page)
    except ValueError as e:
        abort(404, f"{e}") 


    return template('result_page', 
                    user_query=user_query,
                    url_results=url_results, 
                    current_page=page,
                    total_pages = total_pages,
                    **user_info)

