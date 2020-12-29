import re

from . import Mod


HTML_TAG_REGEX = r"<(\w+[^>\n]*)>"


def insert_slash_after_opening_tag_names(output, count=1, include = None, exclude = []):
    p1 = re.compile(HTML_TAG_REGEX)
    p2 = re.compile(r"(\s*)(\w+)([\s\S]*)")

    if include is not None:
        include = [x.lower() for x in include]
    if exclude is not None:
        exclude = [x.lower() for x in exclude]

    def replace_tag_content(tag_content):
        def f(m):
            tag = m.group(2).lower()
            if (include is None and tag not in exclude) or (include is not None and tag in include and tag not in exclude):
                return m.group(1) + m.group(2) + " " + "/" * count + m.group(3)
            else:
                return m.group(1) + m.group(2) + m.group(3)
        tag_content = p2.sub(f, tag_content)
        return tag_content

    output = p1.sub(lambda m: replace_tag_content(m.group()), output)
    return output

mod_insert_slash_after_opening_tag_names = Mod(insert_slash_after_opening_tag_names)