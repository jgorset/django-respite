class Format(object):
    """
    A format represents a file format.
    """

    def __init__(self, name, acronym, extensions, content_types):
        """
        Initialize a new format.

        :param name: A string describing the name of the format (e.g. 'HyperText Markup Language').
        :param acronym: A string describing the acronym of the format (e.g. 'HTML').
        :param extensions: A list of strings describing the extensions of the format (e.g. 'html').
        :param content_types: A list of strings describing the internet media type* of the format (e.g. 'text/html').

        * http://www.iana.org/assignments/media-types/index.html
        """
        self.name = name
        self.acronym = acronym
        self.extensions = extensions
        self.content_types = content_types

    @property
    def extension(self):
        """Return the desired extension for this format."""
        return self.extensions[0]

    @property
    def content_type(self):
        """Return the desired content type for this format."""
        return self.content_types[0]

    def __str__(self):
        return self.name

FORMATS = [
    Format('HyperText Markup Language', 'HTML', ['html'], ['text/html']),
    Format('Extensible Markup Language', 'XML', ['xml'], ['application/xml', 'text/xml']),
    Format('JavaScript Object Notation', 'JSON', ['json'], ['application/json']),
    Format('JavaScript', 'JS', ['js'], ['application/javascript']),
]

def find(identifier):
    """
    Find and return a format by name, acronym or extension.

    :param identifier: A string describing the format.
    """
    for format in FORMATS:
        if identifier in [format.name, format.acronym, format.extension]:
            return format

    raise UnknownFormat('No format found with name, acronym or extension "%s"' % identifier)

def find_by_name(name):
    """
    Find and return a format by name.

    :param name: A string describing the name of the format.
    """
    for format in FORMATS:
        if name == format.name:
            return format

    raise UnknownFormat('No format found with name "%s"' % name)

def find_by_extension(extension):
    """
    Find and return a format by extension.

    :param extension: A string describing the extension of the format.
    """
    for format in FORMATS:
        if extension in format.extensions:
            return format

    raise UnknownFormat('No format found with extension "%s"' % extension)

def find_by_content_type(content_type):
    """
    Find and return a format by content type.

    :param content_type: A string describing the internet media type of the format.
    """
    for format in FORMATS:
        if content_type in format.content_types:
            return format

    raise UnknownFormat('No format found with content type "%s"' % content_type)

class UnknownFormat(Exception):
    pass
