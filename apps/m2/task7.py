from bs4 import BeautifulSoup, SoupReplacer
import sys

if len(sys.argv) < 2:
    print("Usage: python3 task_class.py <filename>")
    sys.exit(1)
filename = sys.argv[1]

with open(filename, "r", encoding="utf-8") as f:
    content = f.read()

add_class = SoupReplacer("p", attrs={"class": "test"})
soup = BeautifulSoup(content, "html.parser", replacer=add_class)

with open("class_output.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print("output stored in class_output.html")