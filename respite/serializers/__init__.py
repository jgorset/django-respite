from respite.serializers.jsonserializer import JSONSerializer
from respite.serializers.xmlserializer import XMLSerializer
from respite import formats

serializers = {
    formats.find('JavaScript Object Notation'): JSONSerializer,
    formats.find('Extensible Markup Language'): XMLSerializer
}
