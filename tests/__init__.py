"""
These are Respite's tests. You may run them with `nose`_::

    $ export DJANGO_SETTINGS_MODULE=tests.project.settings
    $ nosetests

.. _nose: http://readthedocs.org/docs/nose/en/latest/

"""

from django.core.management import call_command

def setup():
    """Setup the test environment."""
    call_command('syncdb', interactive=False)
