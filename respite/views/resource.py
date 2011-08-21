from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.forms import CharField, HiddenInput
from django.forms.models import model_to_dict

from respite.utils import generate_form
from respite.inflector import pluralize, cc2us
from respite.views.views import Views

from respite.decorators import route

class Resource(object):
    """
    A collection of views that facilitate for common features.
    
    :attribute model: A reference to a model.
    :attribute form: A reference to a form, or ``None`` to generate one automatically.
    """
    
    model = None
    form = None

    @route(
        regex = lambda prefix: r'^%s(?:$|index(?:\.[a-zA-Z]+)?$)' % prefix,
        method = 'GET',
        name = lambda views: '%s_%s' % (views.model._meta.app_label, pluralize(cc2us(views.model.__name__)))
    )
    def index(self, request):
        """Render a list of objects."""
        objects = self.model.objects.all()

        return self._render(
            request = request,
            template = 'index',
            context = {
                cc2us(pluralize(self.model.__name__)): objects,
            },
            status = 200
        )

    @route(
        regex = lambda prefix: r'^%s(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?$' % prefix,
        method = 'GET',
        name = lambda views: '%s_%s' % (views.model._meta.app_label, cc2us(views.model.__name__))
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

    @route(
        regex = lambda prefix: r'^%snew(?:\.[a-zA-Z]+)?$' % prefix,
        method = 'GET',
        name = lambda views: 'new_%s_%s' % (views.model._meta.app_label, cc2us(views.model.__name__))
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

    @route(
        regex = lambda prefix: r'^%s(?:$|index(?:\.[a-zA-Z]+)?$)' % prefix,
        method = 'POST',
        name = lambda views: '%s_%s' % (views.model._meta.app_label, pluralize(cc2us(views.model.__name__)))
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

    @route(
        regex = lambda prefix: r'^%s(?P<id>[0-9]+)/edit(?:\.[a-zA-Z]+)?$' % prefix,
        method = 'GET',
        name = lambda views: 'edit_%s_%s' % (views.model._meta.app_label, cc2us(views.model.__name__))
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

    @route(
        regex = lambda prefix: r'^%s(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?$' % prefix,
        method = 'PATCH',
        name = lambda views: '%s_%s' % (views.model._meta.app_label, cc2us(views.model.__name__))
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

        Form = generate_form(
            model = self.model,
            form = self.form,
            fields = tuple(request.PATCH)
        )

        form = Form(request.PATCH, instance=object)
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

    @route(
        regex = lambda prefix: r'^%s(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?$' % prefix,
        method = 'PUT',
        name = lambda views: '%s_%s' % (views.model._meta.app_label, cc2us(views.model.__name__))
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

    @route(
        regex = lambda prefix: r'^%s(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?$' % prefix,
        method = 'DELETE',
        name = lambda views: '%s_%s' % (views.model._meta.app_label, cc2us(views.model.__name__))
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
