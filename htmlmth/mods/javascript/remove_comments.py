import re

from . import Mod


def remove_comments(output):
    output = re.sub(r'(\/\*[\w\'\s\n\*]*\*\/)', r'', output)  # multi-line comments
    output = re.sub(r'((?:[\s;]+)|^)(\/\/.*$)', r'\1', output)  # single-line comments
    return output

mod_remove_comments = Mod(remove_comments)
