from django.core.urlresolvers import reverse
from django.utils import translation

from nose.tools import *

def test_urls():
    url = reverse('articles')
    assert_equal('/news/articles/', url)

    url = reverse('article', args=[1])
    assert_equal('/news/articles/1', url)

    url = reverse('edit_article', args=[1])
    assert_equal('/news/articles/1/edit', url)

    url = reverse('new_article')
    assert_equal('/news/articles/new', url)

def test_localized_urls():
    with translation.override('nb'):
        url = reverse('articles')
        assert_equal('/nyheter/artikler/', url)

        url = reverse('article', args=[1])
        assert_equal('/nyheter/artikler/1', url)

        url = reverse('edit_article', args=[1])
        assert_equal('/nyheter/artikler/1/edit', url)

        url = reverse('new_article')
        assert_equal('/nyheter/artikler/new', url)
