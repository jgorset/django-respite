from django.conf import settings
from django.core.management import call_command

settings.configure(
    DATABASES = {
        'default': {
            'ENGINE': 'sqlite3',
            'NAME': ':memory:'
        }
    },
    INSTALLED_APPS = [
        'respite',
        'tests.news'
    ],
    ROOT_URLCONF = 'tests.urls',
    RESPITE_DEFAULT_FORMAT = 'html',
    MIDDLEWARE_CLASSES = [
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'respite.middleware.HttpPutMiddleware',
        'respite.middleware.HttpPatchMiddleware',
        'respite.middleware.HttpMethodOverrideMiddleware',
        'respite.middleware.JsonMiddleware'
    ]
)

call_command('syncdb')
