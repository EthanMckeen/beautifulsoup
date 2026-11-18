import types

from bs4 import BeautifulSoup
from bs4.element import Comment, Doctype, NavigableString, Tag


def test_visits_every_node_in_document_order():
    soup = BeautifulSoup("<div><p>one</p><b>two</b></div>", "html.parser")
    visited = [n.name if isinstance(n, Tag) else str(n) for n in soup]
    assert visited == ["div", "p", "one", "b", "two"]


def test_yields_tags_strings_comments_and_doctype():
    soup = BeautifulSoup("<!DOCTYPE html><p>text<!--note--></p>", "html.parser")
    assert [type(n) for n in soup] == [Doctype, Tag, NavigableString, Comment]


def test_empty_document_yields_nothing():
    soup = BeautifulSoup("", "html.parser")
    assert list(soup) == []


def test_iteration_is_lazy_and_repeatable():
    soup = BeautifulSoup("<p>a</p><p>b</p>", "html.parser")

    it = iter(soup)
    assert isinstance(it, types.GeneratorType)  # not a prebuilt list
    assert next(it).name == "p"
    assert next(it) == "a"  # produced one at a time

    # A fresh iteration starts from the beginning: p, "a", p, "b"
    assert sum(1 for _ in soup) == 4

    # Stopping early is fine
    for node in soup:
        break


def test_deeply_nested_document_does_not_recurse():
    depth = 1200  # deeper than Python's default recursion limit of 1000
    soup = BeautifulSoup(
        "<div>" * depth + "x" + "</div>" * depth, "html.parser"
    )
    # depth divs plus the one text node
    assert sum(1 for _ in soup) == depth + 1