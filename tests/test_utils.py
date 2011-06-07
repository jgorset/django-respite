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

def test_parse_http_accept_header():
    from respite.utils import parse_http_accept_header

    input = 'application/xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'
    expected_output = ['application/xml', 'image/png', 'text/html', 'text/plain', '*/*']

    assert parse_http_accept_header(input) == expected_output
