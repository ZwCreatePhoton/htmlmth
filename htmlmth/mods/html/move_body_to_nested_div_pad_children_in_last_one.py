import re

from . import Mod


def move_body_to_nested_div_pad_children_in_last_one(N, M, output):
    DIV_LEFT = "DIVLEFT"
    DIV_RIGHT = "DIVRIGHT"
    p = re.compile(r'(?i)(<[^/>]*body[^>]*>)([\s\S]*)(<\s*\/s*body[^>]*>)')
    sub = r'\1' + DIV_LEFT + r'\2' + DIV_RIGHT + r'\3'
    output = re.sub(p, sub, output)
    output = output.replace(DIV_LEFT, "<div>"*(N-1) + "<div></div>"*(M//2 - 1) + "<div>")
    output = output.replace(DIV_RIGHT, "</div>" + "<div></div>"*(M//2 - 1) + "</div>"*(N-1))
    return output

mod_move_body_to_nested_div_pad_children_in_last_one = Mod(move_body_to_nested_div_pad_children_in_last_one)
