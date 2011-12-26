from django import forms

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

def parse_content_type(content_type):
    """
    Return a tuple of content type and charset.

    :param content_type: A string describing a content type.
    """
    if ';' in content_type:
        return content_type.split(';')
    else:
        return content_type, 'ISO-8859-1'

def parse_http_accept_header(header):
    """
    Return a list of content types listed in the HTTP Accept header
    ordered by quality.

    :param header: A string describing the contents of the HTTP Accept header.
    """
    components = [item.strip() for item in header.split(',')]

    l = []
    for component in components:
        if ';' in component:
            subcomponents = [item.strip() for item in component.split(';')]
            l.append(
                (
                    subcomponents[0], # eg. 'text/html'
                    subcomponents[1][2:] # eg. 'q=0.9'
                )
            )
        else:
            l.append((component, '1'))

    l.sort(
        key = lambda i: i[1],
        reverse = True
    )

    content_types = []
    for i in l:
        content_types.append(i[0])

    return content_types
