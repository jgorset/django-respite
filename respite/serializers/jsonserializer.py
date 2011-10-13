try:
    import json
except ImportError:
    from django.utils import simplejson as json
    
from respite.serializers.base import Serializer
    
class JSONSerializer(Serializer):

    def serialize(self):
        data = super(JSONSerializer, self).serialize()

        return json.dumps(data, ensure_ascii=False)
