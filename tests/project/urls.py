from django.conf.urls.defaults import *

from views import home

urlpatterns = patterns('',
    (r'^$', home),
    (r'^news/', include('tests.project.app.urls'))
)
