import re

from . import Mod


def remove_vbscript_comments(output):
    # vbscript comments can not be parsed with only regex
    # so this is not good for edge cases
    output = re.sub(r"\n\t*'[^'\n]*\n", '\n', output)
    output = re.sub(r"\n\t*'[^'\n]*\n", '\n', output)
    output = re.sub(r"\n\t*'[^\"\n]*\n", '\n', output)
    output = re.sub(r"\n\t*'[^\"\n]*\n", '\n', output)
    output = re.sub(r"\t+'[^'\n]*\n", '\n', output)
    output = re.sub(r'\'[^"\n]*\n', '\n', output)
    return output

mod_remove_vbscript_comments = Mod(remove_vbscript_comments)