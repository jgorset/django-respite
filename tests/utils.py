"""Test utilities."""

def monkeypatch_method(cls):
    """Monkeypatch the given function to the given class."""
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator
