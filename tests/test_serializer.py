"""Tests for respite.serializers."""

from respite.serializers.base import Serializer
from respite.utils import generate_form

from news.models import Article

def setup():
    Article.objects.create(
        title = 'Title',
        content = 'Content'
    )
    
    Article.objects.create(
        title = 'Another title',
        content = 'Another content'
    )

def teardown():
    Article.objects.all().delete()

def test_model_serialization():
    article = Article.objects.get(id=1)

    assert Serializer(article).preprocess() == {
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'created_at': article.created_at.isoformat()
    }

def test_queryset_serialization():
    articles = Article.objects.all()

    assert Serializer(articles).preprocess() == [
        {
            'id': articles[0].id,
            'title': articles[0].title,
            'content': articles[0].content,
            'created_at': articles[0].created_at.isoformat()
        },
        {
            'id': articles[1].id,
            'title': articles[1].title,
            'content': articles[1].content,
            'created_at': articles[1].created_at.isoformat()
        }
    ]

def test_form_serialization():
    import django.forms
    
    form = generate_form(Article)()

    assert Serializer(form).preprocess() == {
        'fields': ['title', 'content']
    }
