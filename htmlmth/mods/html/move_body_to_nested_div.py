import re

from . import Mod


def move_body_to_nested_div(N, output):
    p = re.compile(r'(?i)(<[^/>]*body[^>]*>)([\s\S]*)(<\s*\/s*body[^>]*>)')
    sub = r'\1' + '<div>'*N + r'\2' + '</div>'*N + r'\3'
    output = re.sub(p, sub, output)
    return output

mod_move_body_to_nested_div = Mod(move_body_to_nested_div)
