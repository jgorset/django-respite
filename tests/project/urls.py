from django.conf.urls import *
from django.utils.translation import ugettext_lazy as _

from views import home

urlpatterns = patterns('',
    (r'^$', home),
    (_(r'^news/'), include('tests.project.app.urls'))
)
