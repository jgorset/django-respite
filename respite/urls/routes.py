from respite.inflector import pluralize, cc2us

class Route(object):
    """A route instance connects a path and method to a view."""

    def __init__(self, regex, view, method, name):
        """
        Initialize a route.

        Arguments:
        regex   --  A string describing a regular expression to which the request path will be
                    matched, or a function that accepts the parent resource's 'prefix' argument and returns it.
        view    --  A string describing the name of the view to delegate the request to.
        method  --  A string describing the HTTP method that this view accepts.
        name    --  A string describing the name of the URL pattern, or a function that accepts
                    the parent resource's 'views' argument and returns it.
        """
        self.regex = regex
        self.view = view
        self.method = method
        self.name = name

route = Route
