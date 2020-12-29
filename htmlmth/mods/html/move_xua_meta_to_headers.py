import re

from . import Mod
from ..html import remove_html_tag_meta_http_equiv
from ..http import declare_xua


def move_xua_meta_to_headers(output, headers):
    p1 = re.compile('(?i)<meta\s+http-equiv="x.*ua.*compatible".*content="(.*)".*>')
    p2 = re.compile('(?i)<meta\s+content="(.*)".*http-equiv="x.*ua.*compatible".*>')
    if (p1.findall(output)):
        xua_value = p1.findall(output)[0]
    else:
        xua_value = p2.findall(output)[0]
    output = remove_html_tag_meta_http_equiv("x-ua-compatible", output)
    declare_xua(xua_value, headers)
    return output, headers

mod_move_xua_meta_to_headers = Mod(move_xua_meta_to_headers)
