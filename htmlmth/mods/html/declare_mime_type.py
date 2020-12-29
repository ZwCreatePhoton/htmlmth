import re

from . import Mod

# replaces the content-type om the content-type http-equiv meta header
# if one does not exists, one will be inserted in the head of the document

def declare_mime_type(mime_type, output):
    p1 = re.compile('(?i)(<meta\s+http-equiv="content-type".*content=")(.*)(".*>)')
    p2 = re.compile('(?i)(<meta\s+content=")(.*)(".*http-equiv="content-type".*>)')

    def replace_tag_content(m):
        old_content_type = m.group(2)
        p3 = re.compile(r"(\s*)([^;]+)(;*)")
        new_content_type = p3.sub(lambda n: n.group(1) + mime_type + n.group(3), old_content_type)
        return m.group(1) + new_content_type + m.group(2)

    output, success1 = p1.subn(replace_tag_content, output)
    output, success2 = p2.subn(replace_tag_content, output)

    if success1 == 0 and success2 == 0:
        meta_element_str = '<meta http-equiv="content-type" content="{}"/>\n'.format(mime_type)
        p4 = re.compile('(?i)(<\/[^<>]*head[^<>]*>)')
        output, success4 = re.subn(p4, meta_element_str + r"\1", output)
        if success4 == 0:
            p5 = re.compile('(?i)(<[^<>]*body[^<>]*>)')
            output, success4 = re.subn(p5, meta_element_str + r"\1", output)

    return output

mod_declare_mime_type = Mod(declare_mime_type)
