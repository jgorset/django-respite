DATABASES = {
    'default': {
        'ENGINE': 'sqlite3',
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
    'respite',
    'tests.project.app'
]

ROOT_URLCONF = 'tests.project.urls'
