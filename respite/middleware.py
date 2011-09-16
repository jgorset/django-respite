import re

from django.http import QueryDict

class HttpMethodOverrideMiddleware:
    """
    Facilitate for overriding the HTTP method with the X-HTTP-Method-Override
    header or a '_method' HTTP POST parameter.
    """

    def process_request(self, request):
        if request.META.has_key('HTTP_X_HTTP_METHOD_OVERRIDE') \
        or request.POST.has_key('_method'):
            request.method = (
                request.META.get('HTTP_X_HTTP_METHOD_OVERRIDE') or
                request.POST.get('_method')
            ).upper()
            
        if '_method' in request.POST:
            request._raw_post_data = re.sub(r'_method=(PUT|PATCH|DELETE)&?', '', request.raw_post_data)

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
