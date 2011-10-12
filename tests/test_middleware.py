"""Tests for respite.middleware."""

from django.utils import simplejson as json

from tests.client import Client

from respite.middleware import JsonMiddleware

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
