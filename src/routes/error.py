from bottle import template, request
from utils.oauth import get_user_info

def register_error_handlers(app):
    """Registers custom error handlers to the given Bottle app."""

    @app.error(404)
    def error_404(error):
        session = request.environ.get('beaker.session')
        user_info = get_user_info(session)

        # Render the custom error page for 404
        return template(
            'error_page',
            error_message="Page Not Found",
            error_description="The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.",
            **user_info
        )

    @app.error(500)
    def error_500(error):
        session = request.environ.get('beaker.session')
        user_info = get_user_info(session)

        # Render the custom error page for 500
        return template(
            'error_page',
            error_message="Internal Server Error",
            error_description="Something went wrong on our end. We are working to fix it as soon as possible.",
            **user_info
        )
