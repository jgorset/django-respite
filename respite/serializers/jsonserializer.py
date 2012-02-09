try:
    import json
except ImportError:
    from django.utils import simplejson as json
    
from respite.serializers.base import Serializer
    
class JSONSerializer(Serializer):

    def serialize(self, **kwargs):
        data = super(JSONSerializer, self).serialize()

        jsondata = json.dumps(data, ensure_ascii=False)

        request = kwargs.get('request', None)
        if request and request.GET.has_key('jsonp'):
            return '%s(%s)' % (request.GET.get('jsonp'), jsondata)
        else:
            return jsondata