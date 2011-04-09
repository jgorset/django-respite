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
    
def get_content_type(format):
    """
    Determine a content type from a format.
    
    Arguments:
    format -- A string describing a format.
    """
    formats = [
        ('html', 'text/html'),
        ('txt', 'text/plain'),
        ('json', 'application/json'),
        ('xml', 'text/xml')
    ]
    
    for f in formats:
        if f[0] == format:
            return f[1]
            
    raise ValueError('Content type not known for format "%s"' % format)