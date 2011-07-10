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
        method  --  A string describing the HTTP method that this action accepts.
        name    --  A string describing the name of the URL pattern, or a function that accepts
                    the parent resource's 'views' argument and returns it.
        """
        self.regex = regex
        self.view = view
        self.method = method
        self.name = name

route = Route

index = route(
    regex = lambda prefix: r'^%s(?:$|index(?:\.[a-zA-Z]+)?$)' % prefix,
    view = 'index',
    method = 'GET',
    name = lambda views: '%s_%s' % (views.model._meta.app_label, pluralize(cc2us(views.model.__name__)))
)

create = route(
    regex = lambda prefix: r'^%s(?:$|index(?:\.[a-zA-Z]+)?$)' % prefix,
    view = 'create',
    method = 'POST',
    name = lambda views: '%s_%s' % (views.model._meta.app_label, pluralize(cc2us(views.model.__name__)))
)

show = route(
    regex = lambda prefix: r'^%s(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?$' % prefix,
    view = 'show',
    method = 'GET',
    name = lambda views: '%s_%s' % (views.model._meta.app_label, cc2us(views.model.__name__))
)

update = route(
    regex = lambda prefix: r'^%s(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?$' % prefix,
    view = 'update',
    method = 'PUT',
    name = lambda views: '%s_%s' % (views.model._meta.app_label, cc2us(views.model.__name__))
)

delete = route(
    regex = lambda prefix: r'^%s(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?$' % prefix,
    view = 'destroy',
    method = 'DELETE',
    name = lambda views: '%s_%s' % (views.model._meta.app_label, cc2us(views.model.__name__))
)

edit = route(
    regex = lambda prefix: r'^%s(?P<id>[0-9]+)/edit(?:\.[a-zA-Z]+)?$' % prefix,
    view = 'edit',
    method = 'GET',
    name = lambda views: 'edit_%s_%s' % (views.model._meta.app_label, cc2us(views.model.__name__))
)

new = route(
    regex = lambda prefix: r'^%snew(?:\.[a-zA-Z]+)?$' % prefix,
    view = 'new',
    method = 'GET',
    name = lambda views: 'new_%s_%s' % (views.model._meta.app_label, cc2us(views.model.__name__))
)

all = [index, create, show, update, delete, edit, new]

def route(regex, view, method, name):
    """
    Define a route.

    Arguments:
    regex   --  A string describing a regular expression to which the request path will be
                matched, or a function that accepts the parent resource's 'prefix' argument and returns it.
    view    --  A string describing the name of the view to delegate the request to.
    method  --  A string describing the HTTP method that this action accepts.
    name    --  A string describing the name of the URL pattern, or a function that accepts
               the parent resource's 'views' argument and returns it.
    """

    return Route(regex, view, method, name)
