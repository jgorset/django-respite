from respite.inflector import pluralize, cc2us

def route(regex, view, method, name):
    """
    Route the given view.
    
    :param regex: A string describing a regular expression to which the request path will be matched.
    :param view: A string describing the name of the view to delegate the request to.
    :param method: A string describing the HTTP method that this view accepts.
    :param name: A string describing the name of the URL pattern.
    
    ``regex`` may also be a lambda that accepts the parent resource's ``prefix`` argument and returns
    a string describing a regular expression to which the request path will be matched.
    
    ``name`` may also be a lambda that accepts the parent resource's ``views`` argument and returns
    a string describing the name of the URL pattern.
    """
    return _Route(regex, view, method, name)

class _Route(object):

    def __init__(self, regex, view, method, name):
        self.regex = regex
        self.view = view
        self.method = method
        self.name = name
