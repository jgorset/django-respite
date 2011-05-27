import inspect

from django.conf.urls.defaults import *
from inflector import pluralize

HTTP_METHODS = ['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT']

def resource(prefix, view, actions=['index', 'show', 'edit', 'update', 'new', 'create', 'destroy'], custom_actions=[]):
    """
    Generate url patterns for a collection of views.
    
    Arguments:
    prefix -- A string describing the resource's URL prefix (f.ex. 'posts').
    view -- A reference to the class in which views are defined.
    actions -- An optional list of strings describing which of the default actions to route for this resource. Defaults to all.
    custom_actions -- An optional list of custom actions as returned by the `action` function. Defaults to an empty list.
    """
    
    model = view.model
    model_name = view.model().__class__.__name__.lower()
    model_name_plural = pluralize(model_name)
    
    # Default actions defined by respite.views.Views
    urls = [
        url(
            regex = r'%s$|%sindex\.?[a-zA-Z]*$' % (prefix, prefix),
            view = view.dispatch,
            kwargs = {
                'GET': 'index' if 'index' in actions else False,
                'POST': 'create' if 'create' in actions else False,
            },
            name = '%s_%s' % (model._meta.app_label, model_name_plural)
        ),
        url(
            regex = r'%s(?P<id>[0-9]+)\.?[a-zA-Z]*$' % prefix,
            view = view.dispatch,
            kwargs = {
                'GET': 'show' if 'show' in actions else False,
                'PUT': 'update' if 'update' in actions else False,
                'DELETE': 'destroy' if 'destroy' in actions else False
            },
            name = '%s_%s' % (model._meta.app_label, model_name)
        ),
        url(
            regex = r'%s(?P<id>[0-9]+)/edit\.?[a-zA-Z]*$' % prefix,
            view = view.dispatch,
            kwargs = {
                'GET': 'edit' if 'edit' in actions else False
            },
            name = 'edit_%s_%s' % (model._meta.app_label, model_name)
        ),
        url(
            regex = r'%snew\.?[a-zA-Z]*$' % prefix,
            view = view.dispatch,
            kwargs = {
                'GET': 'new' if 'new' in actions else False
            },
            name = 'new_%s_%s' % (model._meta.app_label, model_name)
        )
    ]    
    
    # Custom actions defined in a subclass of respite.views.Views
    for custom_action in custom_actions:
        
        kwargs = {}
        for method in custom_action['methods']:
            kwargs[method] = custom_action['function']
        
        urls.append(
            url(
                regex = r'%s/%s' % (prefix, custom_action['regex']),
                view = view.dispatch,
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
