import re

from . import Mod
from ..html import remove_html_tag_meta_http_equiv

# removes the x-ua-compatiable http-equiv meta header
# and replace with the xml x-ua-compatiable process intstruction

def move_xua_meta_to_xmlpi(output):
    p1 = re.compile('(?i)<meta\s+http-equiv="x.*ua.*compatible".*content="(.*)".*>')
    p2 = re.compile('(?i)<meta\s+content="(.*)".*http-equiv="x.*ua.*compatible".*>')
    if p1.findall(output):
        xua_value = p1.findall(output)[0]
    elif p2.findall(output):
        xua_value = p2.findall(output)[0]
    else:
        return output
    output = remove_html_tag_meta_http_equiv("x-ua-compatible", output)

    xmlpi = '\n<?x-ua-compatible content="{}"?>\n'.format(xua_value)
    p3 = re.compile(r'(?i)(<\?xml[^>]*\?>)([\s\S]*)')

    if "<?xml" in output.lower():
        subst = r'''\1{0}\2'''.format(xmlpi)
        output = re.sub(p3, subst, output)
    else:
        output = xmlpi + output

    return output

mod_move_xua_meta_to_xmlpi = Mod(move_xua_meta_to_xmlpi)
