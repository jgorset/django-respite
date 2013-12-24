"""Tests for respite.middleware."""

from nose.tools import *

from six.moves.urllib.parse import urlencode

from django.utils import simplejson as json
from django.test.client import Client, RequestFactory

from respite.middleware import *

client = Client()

def test_json_middleware():
    request = RequestFactory().post(
        path = '/',
        data = json.dumps({
            'foo': 'foo',
            'bar': 'bar',
            'baz': 'baz',
            'hogera': [
                {'hoge': 'hoge'},
                {'fuga': 'fuga'}
            ]
        }),
        content_type = 'application/json'
    )

    JsonMiddleware().process_request(request)

    assert_equal(request.POST, {
        'foo': ['foo'],
        'bar': ['bar'],
        'baz': ['baz'],
        'hogera': [
            {'hoge': ['hoge']},
            {'fuga': ['fuga']}
        ]
    })

def test_http_method_override_middleware():
    request = RequestFactory().post(
        path = '/',
        data = {
            'foo': 'bar',
            '_method': 'PUT'
        }
    )

    HttpMethodOverrideMiddleware().process_request(request)

    assert_equal(request.method, 'PUT')
    assert_equal(request.POST, {})

def test_http_put_middleware():
    request = RequestFactory().put(
        path = '/',
        data = urlencode({
            'foo': 'bar'
        }),
        content_type = "application/x-www-form-urlencoded"
    )

    HttpPutMiddleware().process_request(request)

    assert_equal(request.PUT, {
        'foo': ['bar']
    })
