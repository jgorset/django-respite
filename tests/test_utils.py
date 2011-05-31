"""Tests for respite.utils."""

import mockdjango

def test_generate_form():
    from respite.utils import generate_form
    from django.db import models

    class Article(models.Model):
        title = models.CharField(max_length=255)
        content = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)

    assert generate_form(Article)

def test_get_content_type():
    from respite.utils import get_content_type

    assert get_content_type('html') == 'text/html'
    assert get_content_type('txt') == 'text/plain'
    assert get_content_type('json') == 'application/json'
    assert get_content_type('xml') == 'text/xml'

def test_get_format():
    from respite.utils import get_format

    assert get_format('text/html') == 'html'
    assert get_format('application/xhtml+xml') == 'html'
    assert get_format('text/plain') == 'txt'
    assert get_format('application/json') == 'json'
    assert get_format('text/xml') ==  'xml'
    assert get_format('application/xml') == 'xml'

def test_parse_http_accept_header():
    from respite.utils import parse_http_accept_header

    input = 'application/xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'
    expected_output = ['application/xml', 'image/png', 'text/html', 'text/plain', '*/*']

    assert parse_http_accept_header(input) == expected_output
