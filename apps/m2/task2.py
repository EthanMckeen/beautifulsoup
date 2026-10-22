from bs4 import BeautifulSoup, SoupStrainer
import sys


if len(sys.argv) < 2:
    print("Usage: python3 M1.py <filename>")
    sys.exit(1)
filename = sys.argv[1]

with open(filename, "r", encoding="utf-8") as f:
    content = f.read()

only_a_tags = SoupStrainer("a")

soup = BeautifulSoup(content, "html.parser", parse_only=only_a_tags)

print("________ALL A TAGS_______\n")
print(soup.prettify)