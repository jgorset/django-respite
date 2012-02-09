try:
    import json
except ImportError:
    from django.utils import simplejson as json

from respite.serializers.jsonserializer import JSONSerializer

class JSONPSerializer(JSONSerializer):

    def serialize(self, request):
        data = super(JSONPSerializer, self).serialize(request)

        if 'callback' in request.GET:
            callback = request.GET['callback']
        else:
            callback = 'callback'

        return '%s(%s)' % (callback, data)
