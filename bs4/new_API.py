class SoupReplacer:
    """Replaces every occurrence of one tag name with another
    while the document is being parsed."""

    def __init__(self, og_tag=None, alt_tag=None, attrs=None,
                 name_xformer=None, attrs_xformer=None, xformer=None):
        self.og_tag = og_tag
        self.alt_tag = alt_tag
        self.attrs = attrs
        self.name_xformer = name_xformer
        self.attrs_xformer = attrs_xformer
        self.xformer = xformer

    def apply(self, tag):
        """Run every configured change on a freshly created tag."""
        new_name = self.name_xformer(tag) if self.name_xformer else None
        new_attrs = self.attrs_xformer(tag) if self.attrs_xformer else None

        # Milestone 2 pair form
        if self.og_tag is not None and tag.name == self.og_tag:
            if self.alt_tag is not None:
                tag.name = self.alt_tag
            if self.attrs is not None:
                tag.attrs.update(self.attrs)

        if new_name is not None:
            tag.name = new_name
        if new_attrs is not None:
            tag.attrs = new_attrs

        # The general-purpose one runs last and sees the result of the above
        if self.xformer is not None:
            self.xformer(tag)