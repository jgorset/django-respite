"""Tests for respite.middleware."""

def test_json_middleware():
    from django.utils import simplejson as json
    from respite.middleware import JsonMiddleware
    from utils import RequestFactory

    rf = RequestFactory()

    payload = {
        'foo': 'foo',
        'bar': 'bar',
        'baz': 'baz'
    }

    request = rf.put('/news/articles', 
        data = json.dumps(payload), 
        content_type = 'application/json; charset=utf-8', 
    )

    JsonMiddleware().process_request(request)

    for k, v in request.PUT.iteritems():
        assert payload.get(k) == v
