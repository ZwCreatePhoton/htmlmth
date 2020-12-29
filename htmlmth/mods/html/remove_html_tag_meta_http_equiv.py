import re

from . import Mod


def remove_html_tag_meta_http_equiv(header, output):
    output = re.sub(r"(?i)\n<meta\s+[^>]*http-equiv.*{0}.*>".format(header), "", output)
    output = re.sub(r"(?i)<meta\s+[^>]*http-equiv.*{0}.*>".format(header), "", output)
    return output

mod_remove_html_tag_meta_http_equiv = Mod(remove_html_tag_meta_http_equiv)