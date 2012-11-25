"""Tests for respite.formats."""

from nose.tools import *
from respite import formats

def test_find():
    format = formats.find('HTML')

    assert_equal('HyperText Markup Language', format.name)

def test_find_by_name():
    format = formats.find_by_name('HyperText Markup Language')

    assert_equal('HyperText Markup Language', format.name)

def test_find_by_extension():
    format = formats.find_by_extension('html')

    assert_equal('HyperText Markup Language', format.name)

def test_find_by_content_type():
    format = formats.find_by_content_type('text/html')

    assert_equal('HyperText Markup Language', format.name)

def test_preferred_extension():
    format = formats.find('HTML')

    assert_equal('html', format.extension)

def test_preferred_content_type():
    format = formats.find('HTML')

    assert_equal('text/html', format.content_type)
