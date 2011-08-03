import re

from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.forms import CharField, HiddenInput
from django.forms.models import model_to_dict
from django.template import TemplateDoesNotExist

from respite.settings import DEFAULT_FORMAT
from respite.utils import generate_form, parse_http_accept_header
from respite.serializers import serializers
from respite.inflector import pluralize, cc2us
from respite import formats

class Views(object):
    model = None
    template_path = ''
    supported_formats = ['html']
    form = None

    def index(self, request):
        """Render a list of objects."""
        objects = self.model.objects.all()

        return self._render(
            request = request,
            template = 'index',
            context = {
                pluralize(self.model.__name__).lower(): objects,
            },
            status = 200
        )

    def show(self, request, id):
        """Render a single object."""
        try:
            object = self.model.objects.get(id=id)
        except self.model.DoesNotExist:
            return render(
                request = request,
                template_name = '404.html',
                status = 404
            )

        return self._render(
            request = request,
            template = 'show',
            context = {
                self.model.__name__.lower(): object
            },
            status = 200
        )

    def new(self, request):
        """Render a form to create a new object."""
        form = (self.form or generate_form(self.model))()

        return self._render(
            request = request,
            template = 'new',
            context = {
                'form': form
            },
            status = 200
        )

    def create(self, request):
        """Create a new object."""    
        form = (self.form or generate_form(self.model))(request.POST)

        if form.is_valid():
            object = form.save()

            response = HttpResponse(status=303)
            response['Location'] = reverse(
                viewname = '%s_%s' % (self.model._meta.app_label, cc2us(self.model.__name__)),
                args = [object.id]
            )
            return response
        else:
            return self._render(
                request = request,
                template = 'new',
                context = {
                    'form': form
                },
                status = 400
            )

    def edit(self, request, id):
        """Render a form to edit an object."""
        try:
            object = self.model.objects.get(id=id)
        except self.model.DoesNotExist:
            return render(
                request = request,
                template_name = '404.html',
                status = 404
            )

        form = (self.form or generate_form(self.model))(instance=object)

        # Add "_method" field to override request method to PUT
        form.fields['_method'] = CharField(required=True, initial='PUT', widget=HiddenInput)

        return self._render(
            request = request,
            template = 'edit',
            context = {
                self.model.__name__.lower(): object,
                'form': form
            },
            status = 200
        )

    def update(self, request, id):
        """Update an object."""
        try:
            object = self.model.objects.get(id=id)
        except self.model.DoesNotExist:
            return render(
                request = request,
                template_name = '404.html',
                status = 404
            )

        data = request.PATCH.copy()
        for field in model_to_dict(object):
            data[field] = data.get(field) or getattr(object, field)

        form = (self.form or generate_form(self.model))(data, instance=object)

        if form.is_valid():
            object = form.save()

            return self.show(request, id)
        else:
            return self._render(
                request = request,
                template = 'edit',
                context = {
                    'form': form
                },
                status = 400
            )

    def replace(self, request, id):
        """Replace an object."""
        try:
            object = self.model.objects.get(id=id)
        except self.model.DoesNotExist:
            return render(
                request = request,
                template_name = '404.html',
                status = 404
            )

        form = (self.form or generate_form(self.model))(request.PUT, instance=object)

        if form.is_valid():
            object = form.save()

            return self.show(request, id)
        else:
            return self._render(
                request = request,
                template = 'edit',
                context = {
                    'form': form
                },
                status = 400
            )

    def destroy(self, request, id):
        """Delete an object."""
        try:
            object = self.model.objects.get(id=id)
            object.delete()
        except self.model.DoesNotExist:
            return render(
                request = request,
                template_name = '404.html',
                status = 404
            )

        return self._render(
            request = request,
            template = 'destroy',
            status = 200
        )

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
            # If the client send '*.*' as accepted format use the DEFAULT_FORMAT if any
            if not '*.*' in request.META['HTTP_ACCEPT']:
                for accepted_content_type in parse_http_accept_header(request.META['HTTP_ACCEPT']):
                    try:
                        format = formats.find_by_content_type(accepted_content_type)
                    except formats.UnknownFormat:
                        continue

                    if format in supported_formats:
                        return format
                    else:
                        continue

        # If none of the formats given in the HTTP 'accept' header are supported by these views,
        # or no HTTP 'accept' header was given at all, or the client accepts all formats, 
        # default to the format given in DEFAULT_FORMAT if that's supported.
        if DEFAULT_FORMAT:
            default_format = formats.find(DEFAULT_FORMAT)
            if default_format in supported_formats:
                return default_format
            else:
                return None

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
