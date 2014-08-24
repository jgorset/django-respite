from django.http.multipartparser import MultiPartParser

from respite import formats

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

def parse_content_type(content_type):
    """
    Return a tuple of content type and charset.

    :param content_type: A string describing a content type.
    """
    if '; charset=' in content_type:
        return tuple(content_type.split('; charset='))
    else:
        if 'text' in content_type:
            encoding = 'ISO-8859-1'
        else:
            try:
                format = formats.find_by_content_type(content_type)
            except formats.UnknownFormat:
                encoding = 'ISO-8859-1'
            else:
                encoding = format.default_encoding or 'ISO-8859-1'

        return (content_type, encoding)

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

def parse_multipart_data(request):
    """
    Parse a request with multipart data.

    :param request: A HttpRequest instance.
    """
    return MultiPartParser(
        META=request.META,
        input_data=StringIO(request.body),
        upload_handlers=request.upload_handlers,
        encoding=request.encoding
    ).parse()
