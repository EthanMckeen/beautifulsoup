class SoupReplacer:
    """Replaces every occurrence of one tag name with another
    while the document is being parsed."""

    def __init__(self, og_tag, alt_tag=None, attrs=None):
        self.og_tag = og_tag
        self.alt_tag = alt_tag
        self.attrs = attrs

    def replace(self, name):
        """Return the replacement name if `name` matches og_tag,
        otherwise return `name` unchanged."""
        if name == self.og_tag:
            return self.alt_tag
        return name

    def replace_attrs(self, name, attrs):
        """Return attrs with the new values added (or overwritten)
        if `name` is the tag we're targeting."""
        if self.attrs is not None and name == self.og_tag:
            new_attrs = dict(attrs) if attrs else {}
            new_attrs.update(self.attrs)
            return new_attrs
        return attrs