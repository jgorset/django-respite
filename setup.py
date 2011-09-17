from distutils.core import setup

setup(
    name = 'respite',
    version = '0.10.4',
    description = "Respite conforms Django to Representational State Transfer (REST)",
    author = "Johannes Gorset",
    author_email = "jgorset@gmail.com",
    url = "http://github.com/jgorset/respite",
    packages = ['respite', 'respite.lib', 'respite.serializers', 'respite.urls', 'respite.views']
)
