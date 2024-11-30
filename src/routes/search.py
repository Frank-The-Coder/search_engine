from bottle import Bottle, request, template, abort
from models.database import get_pages_from_search, save_search
from utils.oauth import get_user_info
from features.autocomplete import get_autocomplete_suggestions, initialize_trie, populate_trie_from_db, get_spellcheck_suggestion
from config import USE_DB

if USE_DB:
    populate_trie_from_db()
else:
    words = ["apple", "application", "appliance", "apply", "aptitude", "apron", "appreciate", "approval", "approach", "apparel", "apocalypse", "apex"]
    initialize_trie(words)


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

    # Check if no results and provide a spell check suggestion
    corrected_query = None
    if not url_results:
        spellcheck_suggestion = get_spellcheck_suggestion(user_query, max_results=1)
        if spellcheck_suggestion:
            corrected_query = spellcheck_suggestion[0]


    return template('result_page', 
                    user_query=user_query,
                    url_results=url_results, 
                    current_page=page,
                    total_pages = total_pages,
                    corrected_query=corrected_query,
                    **user_info)

@search_routes.route('/autocomplete')
def autocomplete():
    query = request.query.q
    suggestions = get_autocomplete_suggestions(query)
    return {'suggestions': suggestions}

@search_routes.route('/spellcheck')
def spellcheck():
    typo = request.query.q
    suggestions = get_spellcheck_suggestion(typo, max_results=1)
    return {'corrected_query': suggestions[0] if suggestions else typo}

