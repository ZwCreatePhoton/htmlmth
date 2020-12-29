import re

from . import Mod


HTML_TAG_REGEX = r"<(\w+\b[^>]*)>"
HTML_ATTR_REGEX = '([\w-]+=["\'][^"\']*["\'])' # wont handle the case where there's a qoute in the attribute value


def reverse_attributes(output):
    p1 = re.compile(HTML_TAG_REGEX)
    p2 = re.compile(HTML_ATTR_REGEX)

    def replace_tag_content(tag_content):
        attributes = p2.findall(tag_content)
        for i in range(len(attributes)):
            tag_content = tag_content.replace(attributes[i], "__POSITION_{}__".format(i))
        for i in range(len(attributes)):
            tag_content = tag_content.replace("__POSITION_{}__".format(i), attributes[-i-1])
        return tag_content

    output = p1.sub(lambda m: replace_tag_content(m.group()), output)
    return output

mod_reverse_attributes = Mod(reverse_attributes)