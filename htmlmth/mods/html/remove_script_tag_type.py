import re

from . import Mod


def remove_script_tag_type(output):
    p = re.compile(r"(?i)(<\s*script.*\s+)(type\s*=\s*[\"'].*[\"'])(.*>)")
    output = re.sub(p, r"\1" + r"\3", output)
    return output

mod_remove_script_tag_type = Mod(remove_script_tag_type)

