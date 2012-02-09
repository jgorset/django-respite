try:
    import json
except ImportError:
    from django.utils import simplejson as json
    
from respite.serializers.jsonserializer import JSONSerializer
    
class JSONPSerializer(JSONSerializer):

    def serialize(self, **kwargs):
        data = super(JSONPSerializer, self).serialize()

        request = kwargs.get('request', None)
        callback = 'callback'
        if request and request.GET.has_key('callback'):
            callback = request.GET.get('callback')

        return '%s(%s)' % (callback, data)
