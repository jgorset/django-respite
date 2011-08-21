"""Tests for respite.serializers."""

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
        author = author
    )

    Article.objects.create(
        title = 'Another title',
        content = 'Another content',
        author = author
    )

def teardown():
    Article.objects.all().delete()

def test_model_serialization():
    article = Article.objects.get(id=1)

    serialized_data = Serializer(article).preprocess()
    
    assert serialized_data['id'] == article.id
    assert serialized_data['title'] == article.title
    assert serialized_data['content'] == article.content
    assert serialized_data['is_published'] == article.is_published
    assert serialized_data['created_at'] == article.created_at.isoformat()

def test_queryset_serialization():
    articles = Article.objects.all()

    serialized_data = Serializer(articles).preprocess()
    
    for i in range(2):
        assert serialized_data[i]['id'] == articles[i].id
        assert serialized_data[i]['title'] == articles[i].title
        assert serialized_data[i]['content'] == articles[i].content
        assert serialized_data[i]['is_published'] == articles[i].is_published
        assert serialized_data[i]['created_at'] == articles[i].created_at.isoformat()

def test_form_serialization():
    import django.forms

    form = generate_form(Article)()

    assert Serializer(form).preprocess() == {
        'fields': ['title', 'content', 'is_published', 'author', 'tags']
    }
