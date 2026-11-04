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

def test_name_xformer_renames_tag():
    html = '<p class="x">one <b>two</b> three</p>'
    replacer = SoupReplacer(
        name_xformer=lambda tag: "blockquote" if tag.name == "b" else tag.name
    )
    soup = BeautifulSoup(html, "html.parser", replacer=replacer)

    assert soup.find("b") is None
    assert soup.blockquote.get_text() == "two"
    # The end tag matched, so "three" is still directly inside the <p>
    assert soup.p.get_text() == "one two three"
    assert soup.blockquote.parent.name == "p"
    # Attributes on other tags are untouched
    assert soup.p["class"] == ["x"]


def test_attrs_xformer_returns_new_attrs():
    html = '<p class="old">one</p><b id="keep">two</b>'
    replacer = SoupReplacer(
        attrs_xformer=lambda tag: {"class": "test"} if tag.name == "p" else tag.attrs
    )
    soup = BeautifulSoup(html, "html.parser", replacer=replacer)

    assert soup.p["class"] == ["test"]
    assert soup.b["id"] == "keep"


def test_xformer_can_change_tag_in_place():
    html = '<p class="x" id="a">one</p>'

    def drop_class(tag):
        if "class" in tag.attrs:
            del tag.attrs["class"]

    soup = BeautifulSoup(html, "html.parser", replacer=SoupReplacer(xformer=drop_class))

    assert soup.p.get("class") is None
    assert soup.p["id"] == "a"


def test_nested_renamed_tags_keep_their_structure():
    html = "<div><b>outer <b>inner</b> tail</b> after</div>"
    replacer = SoupReplacer(
        name_xformer=lambda tag: "blockquote" if tag.name == "b" else tag.name
    )
    soup = BeautifulSoup(html, "html.parser", replacer=replacer)

    assert soup.find("b") is None
    outer = soup.div.blockquote
    inner = outer.blockquote
    assert inner.get_text() == "inner"
    assert outer.get_text() == "outer inner tail"
    # Both end tags matched, so " after" sits directly in the <div>
    assert soup.div.contents[-1] == " after"


def test_all_three_xformers_together():
    html = '<b class="old">hi</b>'
    replacer = SoupReplacer(
        name_xformer=lambda tag: "blockquote" if tag.name == "b" else tag.name,
        attrs_xformer=lambda tag: {"class": "was-" + tag.name},
        xformer=lambda tag: tag.attrs.update({"data-name": tag.name}),
    )
    soup = BeautifulSoup(html, "html.parser", replacer=replacer)

    bq = soup.find("blockquote")
    assert bq is not None
    # name_xformer and attrs_xformer both saw the original <b>
    assert bq["class"] == ["was-b"]
    # xformer runs last, so it saw the already-renamed tag
    assert bq["data-name"] == "blockquote"


def test_identity_transformers_leave_document_unchanged():
    html = '<p class="a b">one <i>two</i></p>'
    replacer = SoupReplacer(
        name_xformer=lambda tag: tag.name,
        attrs_xformer=lambda tag: tag.attrs,
    )
    with_replacer = BeautifulSoup(html, "html.parser", replacer=replacer)
    without_replacer = BeautifulSoup(html, "html.parser")

    assert str(with_replacer) == str(without_replacer)