from bs4 import BeautifulSoup, SoupReplacer


def test_replaces_tag_during_parsing():
    html = "<p>one <b>two</b> three <b>four</b></p>"
    replacer = SoupReplacer("b", "blockquote")
    soup = BeautifulSoup(html, "html.parser", replacer=replacer)

    # No <b> tags are left, and both became <blockquote>
    assert soup.find("b") is None
    blockquotes = soup.find_all("blockquote")
    assert [t.get_text() for t in blockquotes] == ["two", "four"]

    # The structure stays intact: each blockquote closes properly
    # and sits directly inside the <p>
    assert all(t.parent.name == "p" for t in blockquotes)
    assert soup.p.get_text() == "one two three four"


def test_document_without_og_tag_is_unchanged():
    html = "<p>one <i>two</i> three</p>"
    replacer = SoupReplacer("b", "blockquote")

    with_replacer = BeautifulSoup(html, "html.parser", replacer=replacer)
    without_replacer = BeautifulSoup(html, "html.parser")

    assert str(with_replacer) == str(without_replacer)

def test_adds_and_replaces_class_attribute():
    html = '<p>one</p><p class="old">two</p><b>three</b>'
    replacer = SoupReplacer("p", attrs={"class": "test"})
    soup = BeautifulSoup(html, "html.parser", replacer=replacer)

    paragraphs = soup.find_all("p")
    assert len(paragraphs) == 2
    assert all(p["class"] == ["test"] for p in paragraphs)
    assert soup.b.get("class") is None