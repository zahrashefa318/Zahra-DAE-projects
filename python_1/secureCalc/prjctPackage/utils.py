from functools import wraps
from flask import make_response

def nocache(view):
     """
    Decorator to disable caching for a Flask view function.

    This ensures that the browser does not cache the response.
    It modifies the response headers to prevent storing, reusing,
    or validating cached content.

    Usage:
        @app.route('/example')
        @nocache
        def example():
            return "This page will not be cached."
    """
     @wraps(view)
     def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
     return no_cache
