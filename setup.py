from setuptools import setup
from setuptools.compat import execfile

# Include version.py without importing respite/__init__.py which can only be
# imported in a Django context because it imports respite/views.py.
exec(compile(open('respite/version.py', "rb").read(), '', 'exec'), globals(), locals())

setup(
    name = 'django-respite',
    version = __version__,
    description = "Respite conforms Django to Representational State Transfer (REST)",
    long_description = open('README.rst').read(),
    author = "Johannes Gorset",
    author_email = "jgorset@gmail.com",
    url = "http://github.com/jgorset/django-respite",
    packages = ['respite', 'respite.lib', 'respite.serializers', 'respite.urls', 'respite.views', 'respite.utils']
)
