from django import forms

def generate_form(model):
    """
    Generate a form from a model.

    Arguments:
    model -- A Django model.
    """
    _model = model
    class Form(forms.ModelForm):
        class Meta:
            model = _model
    return Form

def parse_http_accept_header(header):
    """
    Return a list of content types listed in the HTTP Accept header
    ordered by quality.

    Arguments:
    header -- A string describing the contents of the HTTP Accept header.
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
