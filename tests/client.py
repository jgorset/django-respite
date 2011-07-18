from urllib import urlencode
from urlparse import urlparse

from django.test.client import Client, FakePayload

class Client(Client):

    def patch(self, path, data, content_type, **extra):
        """Construct a PATCH request."""

        if isinstance(data, dict):
            data = urlencode(data)

        parsed_url = urlparse(path)

        environment = {
            'CONTENT_LENGTH': len(data),
            'CONTENT_TYPE': content_type,
            'PATH_INFO': parsed_url[2],
            'QUERY_STRING': parsed_url[4],
            'REQUEST_METHOD': 'PATCH',
            'wsgi.input': FakePayload(data)
        }

        environment.update(extra)

        return self.request(**environment)
