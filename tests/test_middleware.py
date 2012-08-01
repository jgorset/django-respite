"""Tests for respite.middleware."""

from nose.tools import *

from django.utils import simplejson as json
from django.test.client import Client, RequestFactory

from respite.middleware import JsonMiddleware, HttpMethodOverrideMiddleware

client = Client()

def test_json_middleware():
    response = client.post(
        path = '/',
        data = json.dumps({
            'foo': 'foo',
            'bar': 'bar',
            'baz': 'baz'
        }),
        content_type = 'application/json'
    )

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
