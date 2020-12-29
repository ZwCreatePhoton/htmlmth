import sys

from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform
import htmlmth.mods.html


sys.setrecursionlimit(2000)

def _generate_move_body_to_nested_div_pad_children_in_last_one(*args, **kwargs):
    # maximize number of branches we should return 1 until we are log2(M) away from N
    # where N is the recursion ~limit that IE supports (1044 ish) and M is the maximum-ish number of len("<div></div>") length strings we can pad the document with before IE fails to render in time
    N = kwargs.get("N", 1042)
    M = kwargs.get("M", 1000000)

    return TransformFunction("",
                             "move body content to the inside of a deeply nested div element where the deepest div element is padded with many div elements",
                             mime_type_based_transform({
                                 'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.move_body_to_nested_div_pad_children_in_last_one(N, M, x))
                             }))

move_body_to_nested_div_pad_children_in_last_one = _generate_move_body_to_nested_div_pad_children_in_last_one()
move_body_to_nested_div_pad_children_in_last_one.parameterize = _generate_move_body_to_nested_div_pad_children_in_last_one
