import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

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

INSTALLED_APPS = [
    'django_nose',
    'respite',
    'tests.project.app'
]

LOCALE_PATHS = (
    os.path.join(os.path.dirname(__file__), 'locale'),
)

LANGUAGES = (
    ('nb', 'Norwegian'),
    ('en', 'English')
)

LANGUAGE_CODE = 'en'

ROOT_URLCONF = 'tests.project.urls'

SECRET_KEY = 'my secret'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
