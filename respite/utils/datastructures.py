from django.conf import settings
from django.utils import simplejson as json
from django.utils.datastructures import MultiValueDict
from django.utils.encoding import force_text
from django.http import QueryDict

class NestedQueryDict(QueryDict):
    """
    A QueryDict that allows initialization with a dictionary instead of a query string
    and facilitates for nested dictionaries.
    """
    def __init__(self, data, mutable=False, encoding=None):
        MultiValueDict.__init__(self)
        if not encoding:
            # *Important*: do not import settings any earlier because of note
            # in core.handlers.modpython.
            from django.conf import settings
            encoding = settings.DEFAULT_CHARSET
        self.encoding = encoding

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (list, set)):
                    self.setlistdefault(key, [])
                    items = [NestedQueryDict(item) for item in value]
                    super(MultiValueDict, self).__setitem__(key, items)
                elif isinstance(value, dict):
                    self.appendlist(force_text(key, encoding, errors='replace'),
                                    NestedQueryDict(value))
                else:
                    self.appendlist(force_text(key, encoding, errors='replace'), 
                                    force_text(value, encoding, errors='replace'))

        self._mutable = mutable
