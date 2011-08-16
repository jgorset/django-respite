from functools import wraps

from respite.urls import routes

def override_supported_formats(formats):
    """
    Override the views class' supported formats for the decorated function.

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
    Route the decorated view.

    :param regex: A string describing a regular expression to which the request path will be matched.
    :param method: A string describing the HTTP method that this view accepts.
    :param name: A string describing the name of the URL pattern.
    
    ``regex`` may also be a lambda that accepts the parent resource's ``prefix`` argument and returns
    a string describing a regular expression to which the request path will be matched.
    
    ``name`` may also be a lambda that accepts the parent resource's ``views`` argument and returns
    a string describing the name of the URL pattern.
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
