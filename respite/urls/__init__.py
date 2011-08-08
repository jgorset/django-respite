from copy import deepcopy

from django.conf.urls.defaults import *
from django.http import HttpResponse

from respite.inflector import pluralize, cc2us
from respite.urls import routes

def resource(prefix, views, routes):
    """
    Generate a collection of urlpatterns for a class of views.

    Arguments:
    prefix  --  A string describing the resource's URL prefix (f.ex. 'posts').
    views   --  A reference to the class in which views are defined.
    routes  --  A list of routes to generate URL patterns for.
    """
    routes = deepcopy(routes)

    def dispatch(request, GET=False, POST=False, PUT=False, DELETE=False, PATCH=False, **kwargs):
        """
        Dispatch the request according to the request method and the string contained in
        the corresponding keyword argument.

        For example, if the request method is HTTP GET and the 'GET' argument to this function is
        set to 'index', the 'index' function of the views class will be invoked and returned.

        Arguments:
        request  --  A django.http.HttpRequest object.
        GET      --  A string describing the function to call on HTTP GET.
        POST     --  A string describing the function to call on HTTP POST.
        PUT      --  A string describing the function to call on HTTP PUT.
        DELETE   --  A string describing the function to call on HTTP DELETE.
        """

        # Return HTTP 405 Method Not Allowed if the request method isn't routed
        if request.method == 'GET' and not GET \
        or request.method == 'POST' and not POST \
        or request.method == 'PUT' and not PUT \
        or request.method == 'DELETE' and not DELETE \
        or request.method == 'PATCH' and not PATCH \
        or request.method not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']:
            allowed_methods = []

            if GET:
                allowed_methods.append('GET')
            if POST:
                allowed_methods.append('POST')
            if PUT:
                allowed_methods.append('PUT')
            if DELETE:
                allowed_methods.append('DELETE')

            response = HttpResponse()
            response.status_code = 405
            response['Allow'] = ', '.join(allowed_methods)
            return response

        # Dispatch the request
        if request.method in ['GET', 'HEAD']:
            return getattr(views(), GET)(request, **kwargs)
        if request.method == 'POST':
            return getattr(views(), POST)(request, **kwargs)
        if request.method == 'PUT':
            return getattr(views(), PUT)(request, **kwargs)
        if request.method == 'DELETE':
            return getattr(views(), DELETE)(request, **kwargs)
        if request.method == 'PATCH':
            return getattr(views(), PATCH)(request, **kwargs)
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

    def urlify(routes):
        """
        Transform routes into urlpatterns.

        Arguments:
        routes  --  A list of routes.
        """
        urls = []

        # Route regular expressions and names may be lambdas; expand them.
        for i, route in enumerate(routes):
            if callable(route.regex):
                routes[i].regex = route.regex(prefix)
            else:
                routes[i].regex = '^%s' % prefix + (route.regex[1:] if route.regex[0] == '^' else route.regex)

            if callable(route.name):
                routes[i].name = route.name(views)

        for route in list(routes):

            # Collect this route and its siblings (i.e. routes that share
            # same regular expression) in a dictionary of keys that describe
            # HTTP methods and values that describe the corresponding
            # view function.
            #
            # Example:
            #
            # {
            #   'GET': 'index',
            #   'POST': 'create'
            # }
            kwargs = {}
            for sibling in list(routes):
                if sibling.regex == route.regex:
                    kwargs[sibling.method] = sibling.view
                    routes.remove(sibling)

            urls.append(
                url(
                    regex = route.regex,
                    view = dispatch,
                    kwargs = kwargs,
                    name = route.name
                )
            )

        return urls

    return urlify(routes)
