import re

from . import Mod


REPLACE_TEXT = "REPLACEME"


def prepend_content_into_body(content, output):
    p = re.compile(r'(?i)(<[^/>]*body[^>]*>)([\s\S]*)(<\s*\/s*body[^>]*>)')
    sub = r'\1' + REPLACE_TEXT + r'\2' + r'\3'
    output = re.sub(p, sub, output)
    output = output.replace(REPLACE_TEXT, content)
    return output

mod_prepend_content_into_body = Mod(prepend_content_into_body)