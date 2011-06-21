from respite.serializers.jsonserializer import JSONSerializer
from respite import formats

serializers = {
    formats.find('JavaScript Object Notation'): JSONSerializer
}
