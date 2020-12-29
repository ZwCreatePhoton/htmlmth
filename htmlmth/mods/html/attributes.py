import re

from . import Mod


HTML_TAG_REGEX = r"<\??(\w+\b[^>]*)>"
HTML_ATTR_REGEX = r'([\w\-:]+\s*=\s*["\'][^"\']*["\'])' # wont handle the case where there's a qoute in the attribute value


HTML_ATTR2_DQ_REGEX = '([\w\-:]+\s*=\s*["])([^"]*)(["])' # g2 = attr value
HTML_ATTR2_SQ_REGEX = "([\w\-:]+\s*=\s*['])([^']*)(['])" # g2 = attr value


def attributes_reverse(output):
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

mod_attributes_reverse = Mod(attributes_reverse)


def attributes_insert_newline(output, every_n=1, multiplier=1):
    newlines = "\n" * multiplier

    pattern_tag = re.compile(HTML_TAG_REGEX)
    pattern_attr_dq = re.compile(HTML_ATTR2_DQ_REGEX)
    pattern_attr_sq = re.compile(HTML_ATTR2_SQ_REGEX)

    def replace_attr_value(m):
        value = m.group(2)
        if "id" in m.group(1).lower():
            return m.group()
        elif "style" in m.group(1).lower():
            new_value = value.replace(":", newlines + ":" + newlines).replace(";", newlines + ";" + newlines)
            return m.group(1) + new_value + m.group(3)
        value_chunks = []
        i = 0
        while i < len(value):
            chunk = value[i:i+every_n]
            value_chunks.append(chunk)
            i += every_n
        new_value = newlines.join(value_chunks)
        return m.group(1) + new_value + m.group(3)

    def replace_attr_value_xua(m):
        value = m.group(2)
        new_value = value.replace("=", newlines + "=" + newlines)
        return m.group(1) + new_value + m.group(3)

    def replace_attr_value_script(m):
        if "language" in m.group().lower():
            return m.group()
        elif "type" in m.group().lower():
            return m.group()
        return replace_attr_value(m)

    def replace_tag_content(tag_content):
        if "x-ua-compatible" in tag_content.lower(): # x-ua-compatible gets special treatment
            tag_content = pattern_attr_dq.sub(replace_attr_value_xua, tag_content)
            tag_content = pattern_attr_sq.sub(replace_attr_value_xua, tag_content)
        elif "script" in tag_content.lower()[:10]:
            tag_content = pattern_attr_dq.sub(replace_attr_value_script, tag_content)
            tag_content = pattern_attr_sq.sub(replace_attr_value_script, tag_content)
        else:
            tag_content = pattern_attr_dq.sub(replace_attr_value, tag_content)
            tag_content = pattern_attr_sq.sub(replace_attr_value, tag_content)
        return tag_content

    output = pattern_tag.sub(lambda m: replace_tag_content(m.group()), output)
    return output

mod_attributes_insert_newline = Mod(attributes_insert_newline)