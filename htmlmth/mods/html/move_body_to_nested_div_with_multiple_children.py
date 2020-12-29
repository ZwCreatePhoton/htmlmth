import re

from . import Mod


# child_count_func(n) where n = 1..2..3..N -> number of children at level n out of N
# old body content is inserted to the middle deeply nested div element
def move_body_to_nested_div_with_multiple_children(N, child_count_func, output):
    DIV_LEFT = "DIVLEFT"
    DIV_RIGHT = "DIVRIGHT"
    TEMP_BODY_TEXT = "TEMPBODYTEXT"
    def gen_nested_div_with_childs(n, center):
        if n == N:
            if center:
                return TEMP_BODY_TEXT
            else:
                return ""
        number_of_children = child_count_func(n)
        children = []
        for i in range(number_of_children):
            is_center = False
            if center and i == (number_of_children//2 - (n%2)*(1-(number_of_children%2)) ): # alternate between round up / round down bias when number_of_children is even
                is_center = True
            child = gen_nested_div_with_childs(n+1, is_center)
            children.append(child)
        children_string = "".join(children)
        return "<div>" + children_string + "</div>"


    div_elements = gen_nested_div_with_childs(0, True)
    div_elements_split = div_elements.split(TEMP_BODY_TEXT)

    p = re.compile(r'(?i)(<[^/>]*body[^>]*>)([\s\S]*)(<\s*\/s*body[^>]*>)')
    sub = r'\1' + DIV_LEFT + r'\2' + DIV_RIGHT + r'\3'
    output = re.sub(p, sub, output)
    output = output.replace(DIV_LEFT, div_elements_split[0])
    output = output.replace(DIV_RIGHT, div_elements_split[1])
    return output

mod_move_body_to_nested_div_with_multiple_children = Mod(move_body_to_nested_div_with_multiple_children)
