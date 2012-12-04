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

    url = reverse('preview_article', args=[1])
    assert_equal('/news/articles/1/preview', url)

def test_localized_urls():
    with translation.override('nb'):
        url = reverse('articles')
        assert_equal('/nyheter/artikler/', url)

        url = reverse('article', args=[1])
        assert_equal('/nyheter/artikler/1', url)

        url = reverse('edit_article', args=[1])
        assert_equal('/nyheter/artikler/1/endre', url)

        url = reverse('new_article')
        assert_equal('/nyheter/artikler/ny', url)

        url = reverse('preview_article', args=[1])
        assert_equal('/nyheter/artikler/1/forh%C3%A5ndsvis', url)
