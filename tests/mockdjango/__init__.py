import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.mockdjango.settings'

import django.core.management
django.core.management.call_command('syncdb')
