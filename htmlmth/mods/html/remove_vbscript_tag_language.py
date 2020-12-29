import re

from . import Mod


def remove_vbscript_tag_language(output):
    p = re.compile(r"(?i)(<\s*script.*)(\s+language\s*=\s*[\"'].*vb.*[\"'])(.*>)")
    output = re.sub(p, r"\1" + r"\3", output)
    return output

mod_remove_vbscript_tag_language = Mod(remove_vbscript_tag_language)

