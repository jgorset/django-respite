from respite.serializers.jsonserializer import JSONSerializer
from respite.serializers.jsonpserializer import JSONPSerializer
from respite.serializers.xmlserializer import XMLSerializer
from respite import formats

SERIALIZERS = {
    formats.find('JavaScript Object Notation'): JSONSerializer,
    formats.find('JavaScript'): JSONPSerializer,
    formats.find('Extensible Markup Language'): XMLSerializer
}

def find(format):
    """
    Find and return a serializer for the given format.

    Arguments:
    format -- A Format instance.
    """
    try:
        serializer = SERIALIZERS[format]
    except KeyError:
        raise UnknownSerializer('No serializer found for %s' % format.acronym)

    return serializer

class UnknownSerializer(Exception):
    pass
