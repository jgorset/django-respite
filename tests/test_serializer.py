"""Tests for respite.serializers."""

from datetime import datetime

from respite.serializers.base import Serializer
from respite.utils import generate_form

from news.models import Article, Author, Tag

def setup():
    tag = Tag.objects.create(
        name = 'sports'
    )

    author = Author.objects.create(
        name = 'John Doe'
    )

    article1 = Article.objects.create(
        title = 'Title',
        content = 'Content',
        author = author,
        created_at = datetime(1970, 1, 1)
    )

    article1.tags.add(tag)

    article2 = Article.objects.create(
        title = 'Another title',
        content = 'Another content',
        author = author,
        created_at = datetime(1970, 1, 1)
    )

    article2.tags.add(tag)

def teardown():
    Author.objects.all().delete()
    Article.objects.all().delete()
    Tag.objects.all().delete()

def test_model_serialization():
    article = Article.objects.get(id=1)

    assert Serializer(article).serialize() == {
        'id': 1,
        'title': 'Title',
        'content': 'Content',
        'is_published': False,
        'created_at': '1970-01-01T00:00:00',
        'author': {
            'id': 1,
            'name': 'John Doe'
        },
        'tags': [{
            'id': 1,
            'name': 'sports'
        }]
    }

def test_queryset_serialization():
    articles = Article.objects.all()

    assert Serializer(articles).serialize() == [
        {
            'id': 1,
            'title': 'Title',
            'content': 'Content',
            'is_published': False,
            'created_at': '1970-01-01T00:00:00',
            'author': {
                'id': 1,
                'name': 'John Doe'
            },
            'tags': [{
                'id': 1,
                'name': 'sports'
            }]
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
            },
            'tags': [{
                'id': 1,
                'name': 'sports'
            }]
        }
    ]

def test_serializible_object_serialization():

    class SerializibleClass(object):

        def serialize(self):
            return {
                'key': 'value'
            }

    assert Serializer(SerializibleClass()).serialize() == {
        'key': 'value'
    }

def test_form_serialization():
    import django.forms

    form = generate_form(Article)()

    assert Serializer(form).serialize() == {
        'fields': ['title', 'content', 'is_published', 'created_at', 'author', 'tags']
    }
