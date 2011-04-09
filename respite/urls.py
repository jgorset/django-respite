from django.conf.urls.defaults import *
from inflector import pluralize

def resource(prefix, view, actions=['index', 'show', 'edit', 'update', 'new', 'create', 'destroy']):
    """
    Generate url patterns for a view class.
    
    Arguments:
    prefix -- A string describing the resource's URL prefix (f.ex. 'posts').
    view -- The view class.
    actions -- Route these methods.
    """
    
    model_name = view.model().__class__.__name__.lower()
    model_name_plural = pluralize(model_name)
    
    return patterns('',
        url(
            regex = r'%s/$|%s/index(\.(?P<format>[a-zA-Z]+))?$' % (prefix, prefix),
            view = view.dispatch,
            kwargs = {
                'GET': 'index' if 'index' in actions else False,
                'POST': 'create' if 'create' in actions else False,
            },
            name = model_name_plural
        ),
        url(
            regex = r'%s/(?P<id>[0-9]+)(\.(?P<format>[a-zA-Z]+))?$' % prefix,
            view = view.dispatch,
            kwargs = {
                'GET': 'show' if 'show' in actions else False,
                'PUT': 'update' if 'update' in actions else False,
                'DELETE': 'destroy' if 'destroy' in actions else False
            },
            name = model_name
        ),
        url(
            regex = r'%s/(?P<id>[0-9]+)/edit(\.(?P<format>[a-zA-Z]+))?$' % prefix,
            view = view.dispatch,
            kwargs = {
                'GET': 'edit' if 'edit' in actions else False
            },
            name = 'edit_%s' % model_name
        ),
        url(
            regex = r'%s/new(\.(?P<format>[a-zA-Z]+))?$' % prefix,
            view = view.dispatch,
            kwargs = {
                'GET': 'new' if 'new' in actions else False
            },
            name = 'new_%s' % model_name
        )
    )