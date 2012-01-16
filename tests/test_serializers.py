"""Tests for respite.serializers.*"""

from datetime import datetime

from respite.serializers.base import Serializer
from respite.serializers.jsonserializer import JSONSerializer
from respite.serializers.xmlserializer import XMLSerializer
from respite.utils import generate_form

from .project.app.models import Article, Author, Tag

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
    """Verify that models may be serialized."""
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

    assert JSONSerializer(article).serialize()
    assert XMLSerializer(article).serialize()

def test_queryset_serialization():
    """Verify that querysets may be serialized."""
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
    """Verify that any object that defines a ``serialize`` method may be serialized."""

    class SerializibleClass(object):

        def serialize(self):
            return {
                'key': 'value'
            }

    assert Serializer(SerializibleClass()).serialize() == {
        'key': 'value'
    }

    assert JSONSerializer(SerializibleClass()).serialize()
    assert XMLSerializer(SerializibleClass()).serialize()

def test_form_serialization():
    """Verify that forms may be serialized."""
    import django.forms

    form = generate_form(Article)()

    assert Serializer(form).serialize() == {
        'fields': ['title', 'content', 'is_published', 'created_at', 'author', 'tags']
    }

    assert JSONSerializer(form).serialize()
    assert XMLSerializer(form).serialize()
