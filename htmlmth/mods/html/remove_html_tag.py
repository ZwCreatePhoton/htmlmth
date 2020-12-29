import re

from . import Mod


def remove_html_tag(tag, output):
    output = re.sub(r"(?i)\n<\/?\s*{0}\s*>".format(tag), "", output)
    output = re.sub(r"(?i)<\/?\s*{0}\s*>".format(tag), "", output)
    return output

mod_remove_html_tag = Mod(remove_html_tag)
