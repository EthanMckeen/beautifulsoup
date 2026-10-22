class SoupReplacer:
    """Replaces every occurrence of one tag name with another
    while the document is being parsed."""

    def __init__(self, og_tag, alt_tag):
        self.og_tag = og_tag
        self.alt_tag = alt_tag

    def replace(self, name):
        """Return the replacement name if `name` matches og_tag,
        otherwise return `name` unchanged."""
        if name == self.og_tag:
            return self.alt_tag
        return name