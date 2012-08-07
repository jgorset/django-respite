import inspect

from functools import wraps

from django.http import HttpResponse

from respite.urls import routes

def override_supported_formats(formats):
    """
    Override the views class' supported formats for the decorated function.

    Arguments:
    formats -- A list of strings describing formats, e.g. ``['html', 'json']``.
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

def before(method_name):
    """
    Run the given method prior to the decorated view.

    If you return anything besides ``None`` from the given method,
    its return values will replace the arguments of the decorated
    view.

    If you return an instance of ``HttpResponse`` from the given method,
    Respite will return it immediately without delegating the request to the
    decorated view.

    Example usage::

        class ArticleViews(Views):

            @before('_load')
            def show(self, request, article):
                return self._render(
                    request = request,
                    template = 'show',
                    context = {
                        'article': article
                    }
                )

            def _load(self, request, id):
                try:
                    return request, Article.objects.get(id=id)
                except Article.DoesNotExist:
                    return self._error(request, 404, message='The article could not be found.')

    :param method: A string describing a class method.
    """
    def decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            returns = getattr(self, method_name)(*args, **kwargs)

            if returns is None:
                return function(self, *args, **kwargs)
            else:
                if isinstance(returns, HttpResponse):
                    return returns
                else:
                    return function(self, *returns)
        return wrapper
    return decorator
