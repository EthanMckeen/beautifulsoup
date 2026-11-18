# Milestone-4

## What changed

`BeautifulSoup` objects are now iterable. `for node in soup:` visits every
node in the document (tags, text, comments, doctype) one at a time, in
document order (depth-first). The change is one new method, `__iter__`, on the
`BeautifulSoup` class in `bs4/__init__.py`. `soup` is still the regular object
returned by the constructor.

```python
soup = BeautifulSoup(html_doc, "html.parser")
for node in soup:
    print(node)
```

## Design

- **Generator, no list.** `__iter__` is a generator, so each node is produced
  only when the loop asks for it. The nodes are never collected into a list.
- **Explicit stack, not recursion.** The traversal keeps a stack with one
  iterator per open level. Its size grows with the tree's depth, not with the
  number of nodes. Recursion would fail on very deep documents because of
  Python's recursion limit; the test suite includes a document nested 1200
  levels deep to check this.
- **Root not included.** The document object itself is not yielded, only the
  nodes under it.
- **Only `BeautifulSoup` changed.** Iterating a plain `Tag` (`for child in tag`)
  behaves as before.