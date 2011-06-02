try:
    import json
except ImportError:
    from django.utils import simplejson as json
    
from base import Serializer
    
class JSONSerializer(Serializer):

    def serialize(self):
        """Serialize the model to JSON."""
        data = self.preprocess()

        return json.dumps(data)
