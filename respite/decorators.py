from functools import wraps

def override_supported_formats(formats):
    """
    Override the views class' list of supported formats for a single action.

    Arguments:
    formats -- A list of strings describing formats, e.g. ['html', 'json']
    """
    def decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            self.supported_formats = formats
            return function(self, *args, **kwargs)
        return wrapper
    return decorator
