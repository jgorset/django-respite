from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^news/', include('tests.project.app.urls'))
)
