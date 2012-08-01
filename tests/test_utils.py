"""Tests for respite.utils."""

from nose.tools import *

def test_generate_form():
    from respite.utils import generate_form
    from .project.app.models import Article

    assert generate_form(Article)

def test_parse_http_accept_header():
    from respite.utils import parse_http_accept_header

    input = 'application/xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'
    expected_output = ['application/xml', 'image/png', 'text/html', 'text/plain', '*/*']

    assert parse_http_accept_header(input) == expected_output

def test_parse_content_type():
    from respite.utils import parse_content_type

    assert_equal(('text/html', 'ISO-8859-1'), parse_content_type('text/html'))
    assert_equal(('text/html', 'ISO-8859-4'), parse_content_type('text/html; charset=ISO-8859-4'))
