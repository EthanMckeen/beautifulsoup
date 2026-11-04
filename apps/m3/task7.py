from bs4 import BeautifulSoup, SoupReplacer
import sys

if len(sys.argv) < 2:
    print("Usage: python3 task7.py <filename>")
    sys.exit(1)
filename = sys.argv[1]

with open(filename, "r", encoding="utf-8") as f:
    content = f.read()


def add_test_class(tag):
    """Give every <p> class="test", replacing any existing class.
    Every other tag keeps its attributes."""
    if tag.name == "p":
        new_attrs = dict(tag.attrs)
        new_attrs["class"] = "test"
        return new_attrs
    return tag.attrs


class_setter = SoupReplacer(attrs_xformer=add_test_class)
soup = BeautifulSoup(content, "html.parser", replacer=class_setter)

with open("task7_output.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print("output stored in task7_output.html")