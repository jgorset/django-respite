"""Tests for respite.utils."""

def test_generate_form():
    from respite.utils import generate_form
    from news.models import Article

    assert generate_form(Article)

def test_parse_http_accept_header():
    from respite.utils import parse_http_accept_header

    input = 'application/xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'
    expected_output = ['application/xml', 'image/png', 'text/html', 'text/plain', '*/*']

    assert parse_http_accept_header(input) == expected_output
