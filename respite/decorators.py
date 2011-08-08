from functools import wraps

from respite.urls import routes

def override_supported_formats(formats):
    """
    Override the views class' list of supported formats for a single action.

    Arguments:
    formats -- A list of strings describing formats, e.g. ['html', 'json']
    """
    def decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            self.supported_formats = formats
            return function(self, *args, **kwargs)
        return wrapper
    return decorator

def route(regex, method, name):
    """
    Route the view.

    Arguments:
    regex   --  A string describing a regular expression to which the request path will be
                matched, or a function that accepts the parent resource's 'prefix' argument and returns it.
    method  --  A string describing the HTTP method that this view accepts.
    name    --  A string describing the name of the URL pattern, or a function that accepts
                the parent resource's 'views' argument and returns it.
    """

    def decorator(function):
        function.route = routes.route(
            regex = regex,
            view = function.__name__,
            method = method,
            name = name
        )

        @wraps(function)
        def wrapper(self, *args, **kwargs):
            return function(self, *args, **kwargs)
        return wrapper

    return decorator
