import json

from respite.serializers.base import Serializer

class JSONSerializer(Serializer):

    def serialize(self, request):
        data = super(JSONSerializer, self).serialize(request)

        return json.dumps(data, ensure_ascii=False)
