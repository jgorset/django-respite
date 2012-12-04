from django.core.urlresolvers import reverse

from nose.tools import *

def test_localized_urls():
    url = reverse('articles')
    assert_equal('/news/articles/', url)

    url = reverse('article', args=[1])
    assert_equal('/news/articles/1', url)

    url = reverse('edit_article', args=[1])
    assert_equal('/news/articles/1/edit', url)

    url = reverse('new_article')
    assert_equal('/news/articles/new', url)
