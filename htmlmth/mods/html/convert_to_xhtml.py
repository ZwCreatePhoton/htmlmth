try:
    # Python 2.6-2.7
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3
    from html.parser import HTMLParser
import re

import tidy

from . import Mod


HTML_SCRIPT_TAG_REGEX = r"<script(?:(?!<script)[\w\W])*<\/script>"


def convert_to_xhtml(output, xml_decl=True):
    old_output = output

    tidy_options = {
        "output_xhtml": 1,
        "add_xml_decl": int(xml_decl),
        "indent": 1,
        "tidy-mark": 0,
    }
    output = str(tidy.parseString(output, **tidy_options))

    if "text/javascript" not in old_output:
        output = output.replace('type="text/javascript"', '')

    p1 = re.compile(HTML_SCRIPT_TAG_REGEX)

    def replace_tag_content(tag_content):
        comment_chars = "//"
        h = HTMLParser()
        if "'vbs" in h.unescape(tag_content).lower() or '"vbs' in h.unescape(tag_content).lower():
            comment_chars = "'"
        return tag_content.replace("<![CDATA[", comment_chars + "<![CDATA[").replace("]]>", comment_chars + "]]>")

    output = p1.sub(lambda m: replace_tag_content(m.group()), output)
    return output

mod_convert_to_xhtml = Mod(convert_to_xhtml)
