import re

from urllib import urlencode

from django.http import QueryDict
from django.utils import simplejson as json

from respite.utils import parse_content_type

class HttpMethodOverrideMiddleware:
    """
    Facilitate for overriding the HTTP method with the X-HTTP-Method-Override
    header or a '_method' HTTP POST parameter.
    """

    def process_request(self, request):
        if 'HTTP_X_HTTP_METHOD_OVERRIDE' in request.META \
        or '_method' in request.POST:
            request.method = (
                request.META.get('HTTP_X_HTTP_METHOD_OVERRIDE') or
                request.POST.get('_method')
            ).upper()

            # Proxy the CSRF middleware token to a header for compatibility with non-idempotent
            # methods besides POST.
            if 'csrfmiddlewaretoken' in request.POST:
                request.META.setdefault('HTTP_X_CSRFTOKEN', request.POST['csrfmiddlewaretoken'])

            # In the interest of keeping the request pristine, we discard the "_method" key
            # and set its "POST" attribute to an empty QueryDict.
            if '_method' in request.POST:
                request._raw_post_data = re.sub(r'_method=(PUT|PATCH|DELETE)&?', '', request.raw_post_data)

            request.POST = QueryDict('')

class HttpPutMiddleware:
    """
    Facilitate for HTTP PUT in the same way Django facilitates for HTTP GET
    and HTTP POST; populate a QueryDict instance with the request body in request.PUT.
    """

    def process_request(self, request):
        if request.method == 'PUT':
            request.PUT = QueryDict(request.raw_post_data)

class HttpPatchMiddleware:
    """
    Facilitate for HTTP PATCH in the same way Django facilitates for HTTP GET
    and HTTP POST; populate a QueryDict instance with the request body in request.PATCH.
    """

    def process_request(self, request):
        if request.method == 'PATCH':
            request.PATCH = QueryDict(request.raw_post_data)

class JsonMiddleware:
    """
    Parse JSON in POST, PUT and PATCH requests.
    """

    def process_request(self, request):
        if 'CONTENT_TYPE' in request.META:
            content_type, encoding = parse_content_type(request.META['CONTENT_TYPE'])

            if content_type == 'application/json':
                data = json.loads(request.raw_post_data, encoding)

                if request.method in ['POST', 'PUT', 'PATCH']:
                    setattr(request, request.method, QueryDict(urlencode(data)))
