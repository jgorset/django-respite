import inspect

from django.conf.urls.defaults import *
from django.http import HttpResponse
from respite.inflector import pluralize, cc2us

HTTP_METHODS = ['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT']

def resource(prefix, views, actions=['index', 'show', 'edit', 'update', 'new', 'create', 'destroy'], custom_actions=[], id_regex=r'[0-9]+'):
    """
    Generate url patterns for a collection of views.

    Arguments:
    prefix -- A string describing the resource's URL prefix (f.ex. 'posts').
    views -- A reference to the class in which views are defined.
    actions -- An optional list of strings describing which of the default actions to route for this resource. Defaults to all.
    custom_actions -- An optional list of custom actions as returned by the `action` function. Defaults to an empty list.
    """

    def dispatch(request, GET=False, POST=False, PUT=False, DELETE=False, **kwargs):
        """
        Dispatch the request according to the request method and the string contained in
        the corresponding argument.

        For example, if the request method is HTTP GET and the 'GET' argument to this function is
        set to 'index', the 'index' function of the views class will be invoked and returned.

        Arguments:
        request -- A django.http.HttpRequest object.
        GET -- A string describing the function to call on HTTP GET.
        POST -- A string describing the function to call on HTTP POST.
        PUT -- A string describing the function to call on HTTP PUT.
        DELETE -- A string describing the function to call on HTTP DELETE.
        """

        if request.method == 'OPTIONS':
            map = {}

            if GET:
                map['GET'] = getattr(views(), GET)
            if POST:
                map['POST'] = getattr(views(), POST)
            if PUT:
                map['PUT'] = getattr(views(), PUT)
            if DELETE:
                map['DELETE'] = getattr(views(), DELETE)

            return views().options(request, map, **kwargs)

        # Return HTTP 405 Method Not Allowed if no function is mapped to the request method
        if request.method == 'GET' and not GET \
        or request.method == 'POST' and not POST \
        or request.method == 'PUT' and not PUT \
        or request.method == 'DELETE' and not DELETE:
            allowed_methods = []

            if GET:
                allowed_methods.append('GET')
            if POST:
                allowed_methods.append('POST')
            if PUT:
                allowed_methods.append('PUT')
            if DELETE:
                allowed_methods.append('DELETE')

            response = HttpResponse(status=405)  
            response['Allow'] = ', '.join(allowed_methods)
            return response

        # Dispatch the request
        return getattr(views(), locals()[request.method])(request, **kwargs)

    # Configure URL patterns for default actions (i.e. actions defined in respite.views.Views).
    urls = [
        url(
            regex = r'^%s(?:$|index(?:\.[a-zA-Z]+)?$)' % prefix,
            view = dispatch,
            kwargs = {
                'GET': 'index' if 'index' in actions else False,
                'POST': 'create' if 'create' in actions else False,
            },
            name = '%s_%s' % (views.model._meta.app_label, pluralize(cc2us(views.model.__name__)))
        ),
        url(
            regex = r'^%s(?P<id>%s)(?:\.[a-zA-Z]+)?$' % (prefix, id_regex),
            view = dispatch,
            kwargs = {
                'GET': 'show' if 'show' in actions else False,
                'PUT': 'update' if 'update' in actions else False,
                'DELETE': 'destroy' if 'destroy' in actions else False
            },
            name = '%s_%s' % (views.model._meta.app_label, cc2us(views.model.__name__))
        ),
        url(
            regex = r'^%s(?P<id>%s)/edit(?:\.[a-zA-Z]+)?$' % (prefix, id_regex),
            view = dispatch,
            kwargs = {
                'GET': 'edit' if 'edit' in actions else False
            },
            name = 'edit_%s_%s' % (views.model._meta.app_label, cc2us(views.model.__name__))
        ),
        url(
            regex = r'^%snew(?:\.[a-zA-Z]+)?$' % prefix,
            view = dispatch,
            kwargs = {
                'GET': 'new' if 'new' in actions else False
            },
            name = 'new_%s_%s' % (views.model._meta.app_label, cc2us(views.model.__name__))
        )
    ]    

    # Configure URL patterns for custom actions (i.e. actions defined in a suclass of respite.views.Views).
    for custom_action in custom_actions:

        kwargs = {}
        for method in custom_action['methods']:
            kwargs[method] = custom_action['function']

        urls.append(
            url(
                regex = r'^%s%s$' % (prefix, custom_action['regex']),
                view = dispatch,
                kwargs = kwargs,
                name = custom_action['name']
            )
        )

    return patterns('', *urls)

def action(regex, function, methods, name):
    """
    Define a route to a custom view action.

    Arguments:
    regex -- A string describing a regular expression to which the request path will be matched.
    method -- A list of strings describing HTTP methods that should be routed to this action.
    function -- A string describing the name of the view function to route the request to.
    name -- A string describing the name of the URL pattern.
    """

    if not all([method in HTTP_METHODS for method in methods]):
        raise ValueError('"%s" are not valid HTTP methods.' % '" and "'.join([method for method in methods if not method in HTTP_METHODS]))

    return {
        'regex': regex,
        'function': function,
        'methods': methods,
        'name': name
    }
