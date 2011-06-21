from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# A string describing the format that Respite will fall back to if
# none of the formats the client requested are supported by the view.
#
# Examples:
# DEFAULT_FORMAT = 'HyperText Markup Language'
# DEFAULT_FORMAT = 'HTML'
# DEFAULT_FORMAT = 'html
DEFAULT_FORMAT = getattr(settings, 'RESPITE_DEFAULT_FORMAT', None)
