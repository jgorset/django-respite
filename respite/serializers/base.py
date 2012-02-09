try:
    from collections import OrderedDict
except ImportError:
    from ..lib.ordereddict import OrderedDict

import django.db.models
import django.forms
import datetime

class Serializer(object):
    """Base class for serializers."""

    def __init__(self, source):
        self.source = source

    def serialize(self, request):
        """
        Serialize the given object into into simple
        data types (e.g. lists, dictionaries, strings).
        """

        def serialize(anything):
            
            def serialize_dictionary(dictionary):
                """Dictionaries are serialized recursively."""
                data = OrderedDict()

                # Serialize each of the dictionary's keys
                for key, value in dictionary.items():
                    data.update({ key: serialize(value) })

                return data
                
            def serialize_list(list):
                """Lists are serialized recursively."""
                data = []
                
                # Serialize each of the list's items
                for item in list:
                    data.append(serialize(item))
                    
                return data

            def serialize_queryset(queryset):
                """Querysets are serialized as lists of models."""
                data = []

                # Serialize queryset as a list of models
                for model in queryset:
                    data.append(serialize_model(model))

                return data

            def serialize_manager(manager):
                """Managers are serialized as list of models."""
                data = []

                for model in manager.all():
                    data.append(serialize_model(model))

                return data

            def serialize_model(model):
                """
                Models are serialized by calling their 'serialize' method.

                Models that don't define a 'serialize' method are
                serialized as a dictionary of fields.

                Example:

                    {
                        'id': 1,
                        'title': 'Mmmm pie',
                        'content: 'Pie is good!'
                    }

                """

                if hasattr(model, 'serialize'):
                    return serialize(model.serialize())
                else:
                    data = OrderedDict()
                    for field in model._meta.fields + model._meta.many_to_many:
                        data.update({
                            field.name: serialize(getattr(model, field.name ))
                        })

                    return data

            def serialize_form(form):
                """
                Forms are serialized as a dictionary of fields and errors (if any).

                Example:

                    {
                        'fields': ['title', 'content'],
                        'errors': {
                            'content': 'Must describe pie.'
                        }
                    }

                """
                data = OrderedDict()

                # Serialize form fields as a list of strings
                data['fields'] = []
                for field in form.fields:
                    data['fields'].append(field)

                # Serialize form errors as a dictionary with keys 'field' and 'error'
                if form.errors:
                    data['errors'] = []
                    for field in form:
                        data['errors'].append(
                            {
                                'field': field.name,
                                'error': field.errors.as_text()
                            }
                        )

                return data

            def serialize_date(datetime):
                """Dates are serialized as ISO 8601-compatible strings."""
                return datetime.isoformat()
            
            def serialize_field_file(field_file):
                """Filefields are serialized as strings describing their URL."""
                try:
                    return field_file.url
                except ValueError:
                    return None

            def serialize_image_field_file(image_field_file):
                """Imagefields are serialized as strings describing their URL."""
                try:
                    return image_field_file.url
                except ValueError:
                    return None

            if isinstance(anything, dict):
                return serialize_dictionary(anything)

            if isinstance(anything, list):
                return serialize_list(anything)

            if isinstance(anything, django.db.models.query.QuerySet):
                return serialize_queryset(anything)

            if isinstance(anything, django.db.models.Model):
                return serialize_model(anything)

            if isinstance(anything, (django.forms.Form, django.forms.ModelForm)):
                return serialize_form(anything)

            if isinstance(anything, (str, unicode)):
                return anything

            if isinstance(anything, (int, float, long)):
                return anything

            if isinstance(anything, (datetime.date, datetime.datetime)):
                return serialize_date(anything)

            if isinstance(anything, django.db.models.manager.Manager):
                return serialize_manager(anything)

            if type(anything) is django.db.models.fields.files.FieldFile:
                return serialize_field_file(anything)

            if type(anything) is django.db.models.fields.files.ImageFieldFile:
                return serialize_image_field_file(anything)

            if anything is None:
                return None

            if hasattr(anything, 'serialize'):
                return serialize(anything.serialize())

            raise TypeError("Respite doesn't know how to serialize %s" % anything.__class__.__name__)

        return serialize(self.source)
