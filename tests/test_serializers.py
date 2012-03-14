"""Tests for respite.serializers.*"""

from datetime import datetime

from django.test.client import RequestFactory

from respite.serializers.base import Serializer
from respite.serializers.jsonserializer import JSONSerializer
from respite.serializers.jsonpserializer import JSONPSerializer
from respite.serializers.xmlserializer import XMLSerializer
from respite.utils import generate_form

from .project.app.models import Article, Author, Tag

factory = RequestFactory()

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
    request = factory.get('/')

    assert Serializer(article).serialize(request) == {
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

    assert JSONSerializer(article).serialize(request)
    assert JSONPSerializer(article).serialize(request)
    assert XMLSerializer(article).serialize(request)

def test_queryset_serialization():
    """Verify that querysets may be serialized."""
    articles = Article.objects.all()
    request = factory.get('/')

    assert Serializer(articles).serialize(request) == [
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

    assert JSONSerializer(articles).serialize(request)
    assert JSONPSerializer(articles).serialize(request)
    assert XMLSerializer(articles).serialize(request)

def test_datequeryset_serialization():
    """Verify that datequerysets may be serialized."""
    created_at_dates = Article.objects.all().dates('created_at', 'month')
    request = factory.get('/')

    assert Serializer(created_at_dates).serialize(request) == [
        '1970-01-01T00:00:00'
    ]

    assert JSONSerializer(created_at_dates).serialize(request)
    assert JSONPSerializer(created_at_dates).serialize(request)
    assert XMLSerializer(created_at_dates).serialize(request)

def test_valueslistqueryset_serialization():
    """Verify that valueslistquerysets may be serialized."""
    values_list = Article.objects.all().values_list('is_published')
    request = factory.get('/')

    assert Serializer(values_list).serialize(request) == [
        [
            False
        ],
        [
            False
        ]
    ]

    assert JSONSerializer(values_list).serialize(request)
    assert JSONPSerializer(values_list).serialize(request)
    assert XMLSerializer(values_list).serialize(request)

def test_serializible_object_serialization():
    """Verify that any object that defines a ``serialize`` method may be serialized."""
    request = factory.get('/')

    class SerializibleClass(object):

        def serialize(self):
            return {
                'key': 'value'
            }

    assert Serializer(SerializibleClass()).serialize(request) == {
        'key': 'value'
    }

    assert JSONSerializer(SerializibleClass()).serialize(request)
    assert JSONPSerializer(SerializibleClass()).serialize(request)
    assert XMLSerializer(SerializibleClass()).serialize(request)

def test_form_serialization():
    """Verify that forms may be serialized."""
    import django.forms

    request = factory.get('/')

    form = generate_form(Article)()

    assert Serializer(form).serialize(request) == {
        'fields': ['title', 'content', 'is_published', 'created_at', 'author', 'tags']
    }

    assert JSONSerializer(form).serialize(request)
    assert JSONPSerializer(form).serialize(request)
    assert XMLSerializer(form).serialize(request)
