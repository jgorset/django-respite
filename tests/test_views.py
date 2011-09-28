"""Tests for respite.views."""

from datetime import datetime

from django.conf import settings

from tests.client import Client
from tests.news.models import Article, Author

client = Client()

def setup():
    Article.objects.create(
        title = 'Title',
        content = 'Content',
        author = Author.objects.create(
            name = 'John Doe'
        ),
        created_at = datetime(1970, 1, 1)
    )

def teardown():
    Article.objects.all().delete()

def test_index():
    response = client.get('/news/articles/')
    assert response.status_code == 200

def test_show():
    response = client.get('/news/articles/1.json')

    assert response.status_code == 200

    response = client.get('/news/articles/2')
    assert response.status_code == 404

def test_new():
    response = client.get('/news/articles/new')
    assert response.status_code == 200

def test_create():
    response = client.post('/news/articles/')
    assert response.status_code == 400

    response = client.post('/news/articles/', {
        'title': 'Title',
        'content': 'Content',
        'author': '1',
        'created_at': '1970-01-01 00:00:00'
    })
    assert response.status_code == 201

def test_edit():
    response = client.get('/news/articles/1/edit')
    assert response.status_code == 200

def test_replace():
    from urllib import urlencode

    response = client.put('/news/articles/1')
    assert response.status_code == 400

    response = client.put(
        path = '/news/articles/1.json',
        data = urlencode({
            'title': 'Title',
            'content': 'Content',
            'author': '1',
            'created_at': '1970-01-01 00:00:00'
        }),
        content_type='application/x-www-form-urlencoded'
    )
    assert response.status_code == 200

def test_update():
    response = client.patch(
        path = '/news/articles/1',
        data = {
            'title': 'New title',
            'is_published': 'true'
        },
        content_type='application/x-www-form-urlencoded'
    )

    article = Article.objects.get(id=1)
    assert article.title == 'New title'
    assert article.is_published == True

def test_destroy():
    response = client.delete('/news/articles/1')
    assert response.status_code == 200

def test_custom_action():
    response = client.get('/news/articles/1/preview')
    assert response.status_code == 200

    response = client.get('/news/articles/2/preview')
    assert response.status_code == 404

def test_options():
    response = client.options('/news/articles/', HTTP_ACCEPT='application/json')
    assert response.status_code == 200
    assert set(response['Allow'].split(', ')) == set(['GET', 'POST'])

def test_head():
    response = client.head('/news/articles/1', HTTP_ACCEPT='application/json')
    assert response.status_code == 200
    assert response.content == ''

def test_unsupported_method():
    response = client.post('/news/articles/1')
    assert response.status_code == 405

def test_reverse():
    from django.core.urlresolvers import reverse

    assert reverse('articles')
    assert reverse('article', args=[1])
    assert reverse('edit_article', args=[1])
    assert reverse('new_article')
    assert reverse('preview_article', args=[1])

def test_content_types():
    from django.conf import settings
    from respite import formats
    from news.views import ArticleViews

    response = client.get('/news/articles/1', HTTP_ACCEPT='*/*,application/json')
    assert response['Content-Type'] == '%s; charset=%s' % (
        formats.find(ArticleViews.supported_formats[0]).content_type,
        settings.DEFAULT_CHARSET
    )

    response = client.get('/news/articles/1', HTTP_ACCEPT='unsupported/format, */*')
    assert response['Content-Type'] == '%s; charset=%s' % (
        formats.find(ArticleViews.supported_formats[0]).content_type,
        settings.DEFAULT_CHARSET
    )
