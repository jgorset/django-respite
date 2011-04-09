from django.shortcuts import render
from django.http import HttpResponse

from utils import generate_form, get_content_type
from inflector import pluralize

class View(object):
    model = None
    template_path = ''
    supported_formats = ['html', 'json']
    default_format = 'html'
    
    @classmethod
    def dispatch(self, request, format, GET=False, POST=False, PUT=False, DELETE=False, **kwargs):
        """
        Dispatch the request to the corresponding view method.

        Arguments:
        request -- A Django HTTP request object.
        GET -- A string describing the view function to call on HTTP GET.
        POST -- A string describing the view function to call on HTTP POST.
        PUT -- A string describing the view function to call on HTTP PUT.
        DELETE -- A string describing the view function to call on HTTP DELETE.
        """

        # Return 405 Method Not Allowed if the requested method is not available
        if request.method == 'GET' and not GET \
        or request.method == 'POST' and not POST \
        or request.method == 'PUT' and not PUT \
        or request.method == 'DELETE' and not DELETE:
            allowed_methods = []

            if GET:
                allowed_methods.append('GET')
            if POST:
                allowed_methods.append('POST')
            if PUT:
                allowed_methods.append('PUT')
            if DELETE:
                allowed_methods.append('DELETE')

            response = HttpResponse(status=405)  
            response['Allow'] = ', '.join(allowed_methods)
            return response
        
        if not format:
            format = self.default_format    
        
        # Return 406 Not Acceptable if the requested format is not available
        if not format in self.supported_formats:
            return HttpResponse(status=406)

        # Dispatch the request
        if request.method == 'GET':
            return getattr(self(request, format, **kwargs), GET)()
        if request.method == 'POST':
            return getattr(self(request, format, **kwargs), POST)()
        if request.method == 'PUT':
            return getattr(self(request, format, **kwargs), PUT)()
        if request.method == 'DELETE':
            return getattr(self(request, format, **kwargs), DELETE)()
    
    def __init__(self, request, format=default_format, **kwargs):
        self.request = request
        self.format = format
        
        for key in kwargs:
            self.__dict__[key] = kwargs[key]
            
    def index(self):
        """Render a list of objects."""
        objects = self.model.objects.all()
        
        return self._render(
            template = 'index',
            context = {
                pluralize(self.model.__name__).lower(): objects,
            },
            status = 200
        )
        
    def show(self):
        """Render a single object."""
        object = self.model.objects.get(id=self.id)
        
        return self._render(
            template = 'show',
            context = {
                self.model.__name__.lower(): object
            },
            status = 200
        )
        
    def new(self):
        """Render a form to create a new object."""
        form = generate_form(self.model)()
        
        return self._render(
            template = 'new',
            context = {
                'form': form
            },
            status = 200
        )
        
    def create(self):
        """Create a new object."""
        form = generate_form(self.model)(self.request.POST)
        
        if form.is_valid():
            object = form.save()
            
            response = HttpResponse(status=303)
            response['Location'] = object.get_absolute_url()
            return response
        else:
            return self._render(
                template = 'new',
                context = {
                    'form': form
                },
                status = 400
            )
        
    def edit(self):
        """Render a form to edit an object."""
        object = self.model.objects.get(id=self.id)
        form = generate_form(self.model)(instance=object)
        
        return self._render(
            template = 'edit',
            context = {
                self.model.__name__.lower(): object,
                'form': form
            },
            status = 200
        )
        
    def update(self):
        """Edit an object."""
        object = self.model.objects.get(id=self.id)
        form = generate_form(self.model)(self.request.PUT, instance=object)
        
        if form.is_valid():
            object = form.save()
            
            return self._render(
                template = 'show',
                context = {
                    self.model.__name__.lower(): object
                },
                status = 200
            )
        else:
            return self._render(
                template = 'edit',
                context = {
                    'form': form
                },
                status = 400
            )
            
    def destroy(self):
        """Delete an object."""
        object = self.model.objects.get(id=self.id)
        object.delete()
        
        return self._render(
            template = 'destroy',
            status = 200
        )
    
    def _render(self, template, status, context={}):
        """Render a response."""
        return render(
            request = self.request,
            template_name = '%s/%s.%s' % (self.template_path, template, self.format),
            dictionary = context,
            status = status,
            content_type = get_content_type(self.format)
        )