from bs4 import BeautifulSoup, SoupReplacer
import sys

if len(sys.argv) < 2:
    print("Usage: python3 M1.py <filename>")
    sys.exit(1)
filename = sys.argv[1]

with open(filename, "r", encoding="utf-8") as f:
    content = f.read()

change = SoupReplacer("b", "blockquote")
print("replacing <b> with <bodyquote>\n")
soup = BeautifulSoup(content, "html.parser", replacer=change)

with open("pretty_output.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print("output stored in pretty_output.html\n")