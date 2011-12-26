from setuptools import setup

setup(
    name = 'django-respite',
    version = '1.0.0',
    description = "Respite conforms Django to Representational State Transfer (REST)",
    author = "Johannes Gorset",
    author_email = "jgorset@gmail.com",
    url = "http://github.com/jgorset/respite",
    packages = ['respite', 'respite.lib', 'respite.serializers', 'respite.urls', 'respite.views']
)
