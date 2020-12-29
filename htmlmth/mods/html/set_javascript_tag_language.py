import re

from . import Mod


def set_javascript_tag_language(lang, output):
    p1 = re.compile(r"(?i)(<\s*script.*language\s*=\s*[\"'])(.*j.*)([\"'].*>)")
    output = re.sub(p1, r"\1" + lang + r"\3", output)

    p2 = re.compile(r"(?i)(<\s*script\s+)((?:(?!language\s*=).)*\s*[\"'])(.*j.*)([\"'].*>)")
    output = re.sub(p2, r"\1" + 'language="{}" '.format(lang) + r"\2" + r"\3" + r"\4", output)

    return output

mod_set_javascript_tag_language = Mod(set_javascript_tag_language)
