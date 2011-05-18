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
    Determine the content type from a format.
    
    Arguments:
    format -- A string describing a format.
    """
    formats = [
        ('html', 'text/html'),
        ('html', 'application/xhtml+xml'),
        ('txt', 'text/plain'),
        ('json', 'application/json'),
        ('xml', 'text/xml'),
        ('xml', 'application/xml')
    ]
    
    for f in formats:
        if f[0] == format:
            return f[1]
            
    raise ValueError('Content type not known for format "%s"' % format)
    
def get_format(content_type):
    """
    Determine the format from a content type.
    
    Arguments:
    format -- A string describing a format.
    """
    content_types = [
        ('text/html', 'html'),
        ('application/xhtml+xml', 'html'),
        ('text/plain', 'txt'),
        ('application/json', 'json'),
        ('text/xml', 'xml'),
        ('application/xml', 'xml')
    ]
    
    for s in content_types:
        if s[0] == content_type:
            return s[1]
            
    raise ValueError('Content type not known for format "%s"' % format)
    
def parse_http_accept_header(header):
    """
    Return a list of content types listed in the HTTP Accept header
    ordered by quality.
    
    Arguments:
    header -- A string describing the contents of the HTTP Accept header.
    """
    components = header.split(',')
    
    l = []
    for component in components:
        if ';' in component:
            subcomponents = component.split(';')
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
