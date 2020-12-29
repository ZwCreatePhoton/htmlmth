import re

from . import Mod


def remove_html_comments(output):
    output = re.sub(r'-->\n\n', '-->\n', output)
    output = re.sub(r'<!--.*-->\n', '', output)
    output = re.sub(r'<!--.*-->', '', output)
    return output

mod_remove_html_comments = Mod(remove_html_comments)