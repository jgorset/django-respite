from django.shortcuts import render
from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from django.conf import settings

from respite.settings import DEFAULT_FORMAT
from respite.utils import parse_http_accept_header
from respite import serializers
from respite import formats

class Views(object):
    """
    Base class for views.
    
    :attribute template_path: A string describing a path to prefix templates with, or ``''`` by default.
    :attribute supported_formats: A list of strings describing formats supported by these views, or ``['html']`` by default.
    """
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

        :param request: A django.http.HttpRequest instance.

        Formats specified by extension (e.g. '/articles/index.html') take precedence over formats
        given in the HTTP Accept header, even if it's a format that isn't known by Respite.

        If the request doesn't specify a format by extension (e.g. '/articles/' or '/articles/new')
        and none of the formats in the HTTP Accept header are supported, Respite will fall back
        on the format given in DEFAULT_FORMAT.
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

                # Default to the view's preferred format for the wilcard content type.
                if accepted_content_type == '*/*':
                    return supported_formats[0]

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

    def _render(self, request, template=None, status=200, context={}, headers={}, prefix_template_path=True):
        """
        Render a HTTP response.
        
        :param request: A django.http.HttpRequest instance.
        :param template: A string describing the path to a template.
        :param status: An integer describing the HTTP status code to respond with.
        :param context: A dictionary describing variables to populate the template with.
        :param headers: A dictionary describing HTTP headers.
        :param prefix_template_path: A boolean describing whether to prefix the template with the view's template path.
        
        Please note that ``template`` must not specify an extension, as one will be appended
        according to the request format. For example, a value of ``blog/posts/index``
        would populate ``blog/posts/index.html`` for requests that query the resource's
        HTML representation.
        
        If no template that matches the request format exists at the given location, or if ``template`` is ``None``,
        Respite will attempt to serialize the template context automatically. You can change the way your models
        are serialized by defining ``serialize`` methods that return a dictionary::
        
            class NuclearMissile(models.Model):
                serial_number = models.IntegerField()
                is_armed = models.BooleanField()
                launch_code = models.IntegerField()
                
                def serialize(self):
                    return {
                        'serial_number': self.serial_number,
                        'is_armed': self.is_armed
                    }
        
        If the request format is not supported by the view (as determined by the ``supported_formats``
        property or a specific view's ``override_supported_formats`` decorator), this function will
        yield HTTP 406 Not Acceptable.
        """

        format = self._get_format(request)

        # Render 406 Not Acceptable if the requested format isn't supported.
        if not format:
            return HttpResponse(status=406)

        if template:

            if prefix_template_path:
                template_path = '%s.%s' % (self.template_path + template, format.extension)
            else:
                template_path = '%s.%s' % (template, format.extension)

            try:
                response = render(
                    request = request,
                    template_name = template_path,
                    dictionary = context,
                    status = status,
                    content_type = '%s; charset=%s' % (format.content_type, settings.DEFAULT_CHARSET)
                )
            except TemplateDoesNotExist:
                response = HttpResponse(
                    content = serializers.find(format)(context).serialize(request),
                    content_type = '%s; charset=%s' % (format.content_type, settings.DEFAULT_CHARSET),
                    status = status
                )
        else:
            response = HttpResponse(
                content = serializers.find(format)(context).serialize(request),
                content_type = '%s; charset=%s' % (format.content_type, settings.DEFAULT_CHARSET),
                status = status
            )

        for header, value in headers.items():
            response[header] = value

        return response
