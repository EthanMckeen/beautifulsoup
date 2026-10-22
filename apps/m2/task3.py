from bs4 import BeautifulSoup, SoupStrainer
import sys


if len(sys.argv) < 2:
    print("Usage: python3 M1.py <filename>")
    sys.exit(1)
filename = sys.argv[1]

with open(filename, "r", encoding="utf-8") as f:
    content = f.read()

all_tags = SoupStrainer(True)

soup = BeautifulSoup(content, "html.parser", parse_only=all_tags)

print("________ALL TAGS_______\n")
print(soup.prettify)