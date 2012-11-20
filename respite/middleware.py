import re

from urllib import urlencode
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.http import QueryDict
from django.http.multipartparser import MultiPartParser
from django.utils import simplejson as json

from respite.utils import parse_content_type

def parse_multipart_data(request):
    """Parse a request with multipart data"""
    data = StringIO(request.raw_post_data)
    parser = MultiPartParser(request.META, data, request.upload_handlers, request.encoding)
    return parser.parse()

class HttpMethodOverrideMiddleware:
    """
    Facilitate for overriding the HTTP method with the X-HTTP-Method-Override
    header or a '_method' HTTP POST parameter.
    """

    def process_request(self, request):
        # In the interest of keeping the request pristine, we discard the "_method" key.
        request._raw_post_data = re.sub(r'_method=(GET|POST|PUT|PATCH|DELETE|OPTIONS)&?', '', request.raw_post_data)
        
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

            request.POST = QueryDict('')

class HttpPutMiddleware:
    """
    Facilitate for HTTP PUT in the same way Django facilitates for HTTP GET
    and HTTP POST; populate a QueryDict instance with the request body in request.PUT.
    """

    def process_request(self, request):
        if request.method == 'PUT':
            # If the request contains multipart data we need to parse the request body. 
            if request.META.get('CONTENT_TYPE', '').startswith('multipart'):
                request.PUT = parse_multipart_data(request)[0]
            else:
                request.PUT = QueryDict(request.raw_post_data)

class HttpPatchMiddleware:
    """
    Facilitate for HTTP PATCH in the same way Django facilitates for HTTP GET
    and HTTP POST; populate a QueryDict instance with the request body in request.PATCH.
    """

    def process_request(self, request):
        if request.method == 'PATCH':
            # If the request contains multipart data we need to parse the request body. 
            if request.META.get('CONTENT_TYPE', '').startswith('multipart'):
                request.PATCH = parse_multipart_data(request)[0]
            else:
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
