from django import forms

from parsers import *

def generate_form(model, form=None, fields=False, exclude=False):
    """
    Generate a form from a model.

    :param model: A Django model.
    :param form: A Django form.
    :param fields: A list of fields to include in this form.
    :param exclude: A list of fields to exclude in this form.
    """
    _model, _fields, _exclude = model, fields, exclude

    class Form(form or forms.ModelForm):
        class Meta:
            model = _model

            if _fields is not False:
                fields = _fields

            if _exclude is not False:
                exclude = _exclude

    return Form