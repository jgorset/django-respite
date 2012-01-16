"""Tests for respite.views."""

from datetime import datetime

from nose.tools import with_setup
from django.conf import settings
from django.test.client import Client

from . import monkeys
from .project.app.models import Article, Author

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

@with_setup(setup, teardown)
def test_index():
    response = client.get('/news/articles/')
    assert response.status_code == 200

@with_setup(setup, teardown)
def test_show():
    response = client.get('/news/articles/1.json')

    assert response.status_code == 200

    response = client.get('/news/articles/2', HTTP_ACCEPT='application/json')
    assert response['Content-Type'] == 'application/json; charset=%s' % settings.DEFAULT_CHARSET
    assert response.status_code == 404

    response = client.get('/news/articles/2', HTTP_ACCEPT='text/html')
    assert response['Content-Type'] == 'text/html; charset=%s' % settings.DEFAULT_CHARSET
    assert response.status_code == 404

@with_setup(setup, teardown)
def test_new():
    response = client.get('/news/articles/new')
    assert response.status_code == 200

@with_setup(setup, teardown)
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

@with_setup(setup, teardown)
def test_edit():
    response = client.get('/news/articles/1/edit')
    assert response.status_code == 200

@with_setup(setup, teardown)
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

@with_setup(setup, teardown)
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

@with_setup(setup, teardown)
def test_destroy():
    response = client.delete('/news/articles/1')
    assert response.status_code == 200

@with_setup(setup, teardown)
def test_custom_action():
    response = client.get('/news/articles/1/preview')
    assert response.status_code == 200

@with_setup(setup, teardown)
def test_options():
    response = client.options('/news/articles/', HTTP_ACCEPT='application/json')
    assert response.status_code == 200
    assert set(response['Allow'].split(', ')) == set(['GET', 'POST'])

@with_setup(setup, teardown)
def test_head():
    response = client.head('/news/articles/1', HTTP_ACCEPT='application/json')
    assert response.status_code == 200
    assert response.content == ''

@with_setup(setup, teardown)
def test_unsupported_method():
    response = client.post('/news/articles/1')
    assert response.status_code == 405

@with_setup(setup, teardown)
def test_reverse():
    from django.core.urlresolvers import reverse

    assert reverse('articles')
    assert reverse('article', args=[1])
    assert reverse('edit_article', args=[1])
    assert reverse('new_article')
    assert reverse('preview_article', args=[1])

@with_setup(setup, teardown)
def test_content_types():
    from django.conf import settings
    from respite import formats
    from .project.app.views import ArticleViews

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
