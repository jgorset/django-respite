from django.shortcuts import render
from django.http import HttpResponse
from django.template import TemplateDoesNotExist

from respite.settings import DEFAULT_FORMAT
from respite.utils import parse_http_accept_header
from respite.serializers import serializers
from respite import formats

class Views(object):
    template_path = ''
    supported_formats = ['html']

    def options(self, request, map, *args, **kwargs):
        """List communication options."""
        options = {}
        for method, function in map.items():
            options[method] = function.__doc__

        return self._render(
            request = request,
            template = None,
            context = {
                'options': options
            },
            status = 200,
            headers = {
                'Allow': ', '.join(options.keys())
            }
        )

    def _get_format(self, request):
        """
        Determine and return a 'formats.Format' instance describing the most desired response format
        that is supported by these views.

        Formats specified by extension (e.g. '/articles/index.html') take precedence over formats
        given in the HTTP Accept header, even if it's a format that isn't known by Respite.

        If the request doesn't specify a format by extension (e.g. '/articles/' or '/articles/new')
        and none of the formats in the HTTP Accept header are supported, Respite will fall back
        on the format given in DEFAULT_FORMAT.

        Arguments:
        request -- The request object.
        """

        # Derive a list of 'formats.Format' instances from the list of formats these views support.
        supported_formats = [formats.find(format) for format in self.supported_formats]

        # Determine format by extension...
        if '.' in request.path:
            extension = request.path.split('.')[-1]

            try:
                format = formats.find_by_extension(extension)
            except formats.UnknownFormat:
                return None

            return format if format in supported_formats else None

        # Determine format by HTTP Accept header...
        if 'HTTP_ACCEPT' in request.META:

            # Parse the HTTP Accept header, returning a list of accepted content types sorted by quality
            for accepted_content_type in parse_http_accept_header(request.META['HTTP_ACCEPT']):

                # Default to the format given in DEFAULT_FORMAT for the '*/*' content type.
                if accepted_content_type == '*/*' and DEFAULT_FORMAT:
                    default_format = formats.find(DEFAULT_FORMAT)
                    if default_format in supported_formats:
                        return default_format

                try:
                    format = formats.find_by_content_type(accepted_content_type)
                except formats.UnknownFormat:
                    continue

                if format in supported_formats:
                    return format
                else:
                    continue

        # If none of the formats given in the HTTP 'accept' header are supported by these views,
        # or no HTTP 'accept' header was given at all, default to the format given in
        # DEFAULT_FORMAT if that's supported.
        if DEFAULT_FORMAT:
            default_format = formats.find(DEFAULT_FORMAT)
            if default_format in supported_formats:
                return default_format

    def _render(self, request, template=None, status=200, context={}, headers={}):
        """Render a response."""

        format = self._get_format(request)

        # Render 406 Not Acceptable if the requested format isn't supported.
        if not format:
            return HttpResponse(status=406)

        # Render template...
        try:
            response = render(
                request = request,
                template_name = '%s%s.%s' % (self.template_path, template, format.extension),
                dictionary = context,
                status = status,
                content_type = format.content_type
            )
        # ... or if no template exists, look for an appropriate serializer.
        except TemplateDoesNotExist:

            if format in serializers:
                response = HttpResponse(
                    content = serializers[format](context).serialize(),
                    content_type = format.content_type,
                    status = status
                )
            elif template:
                raise
            else:
                response = HttpResponse()

        for header, value in headers.items():
            response[header] = value

        return response
