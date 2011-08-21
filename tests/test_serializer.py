"""Tests for respite.serializers."""

from datetime import datetime

from respite.serializers.base import Serializer
from respite.utils import generate_form

from news.models import Article, Author

def setup():
    author = Author.objects.create(
        name = 'John Doe'
    )
    
    Article.objects.create(
        title = 'Title',
        content = 'Content',
        author = author,
        created_at = datetime(1970, 1, 1)
    )

    Article.objects.create(
        title = 'Another title',
        content = 'Another content',
        author = author,
        created_at = datetime(1970, 1, 1)
    )

def teardown():
    Author.objects.all().delete()
    Article.objects.all().delete()

def test_model_serialization():
    article = Article.objects.get(id=1)

    assert Serializer(article).preprocess() == {
        'id': 1,
        'title': 'Title',
        'content': 'Content',
        'is_published': False,
        'created_at': '1970-01-01T00:00:00',
        'author': {
            'id': 1,
            'name': 'John Doe'
        }
    }

def test_queryset_serialization():
    articles = Article.objects.all()

    assert Serializer(articles).preprocess() == [
        {
            'id': 1,
            'title': 'Title',
            'content': 'Content',
            'is_published': False,
            'created_at': '1970-01-01T00:00:00',
            'author': {
                'id': 1,
                'name': 'John Doe'
            }
        },
        {
            'id': 2,
            'title': 'Another title',
            'content': 'Another content',
            'is_published': False,
            'created_at': '1970-01-01T00:00:00',
            'author': {
                'id': 1,
                'name': 'John Doe'
            }
        }
    ]


def test_form_serialization():
    import django.forms

    form = generate_form(Article)()

    assert Serializer(form).preprocess() == {
        'fields': ['title', 'content', 'is_published', 'created_at', 'author', 'tags']
    }
