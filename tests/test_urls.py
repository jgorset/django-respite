from django.core.urlresolvers import reverse

from nose.tools import *

def test_localized_urls():
    url = reverse('articles')
    assert_equal('/news/articles/', url)
