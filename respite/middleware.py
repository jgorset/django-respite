from django.http import QueryDict

class HTTPMethodOverrideMiddleware:
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

class HTTPPUTMiddleware:
    """
    Facilitate for HTTP PUT in the same way Django facilitates for HTTP GET
    and HTTP POST; populate a QueryDict instance with the request body in request.PUT.
    """

    def process_request(self, request):
        if request.method == 'PUT':
            request.PUT = QueryDict(request.raw_post_data)
