import math
import sys

from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform
import htmlmth.mods.html



sys.setrecursionlimit(2000)

def _generate_move_body_to_nested_div_with_children(*args, **kwargs):
    # maximize number of branches we should return 1 until we are log2(M) away from N
    # where N is the recursion ~limit that IE supports (1044 ish) and M is the maximum-ish number of len("<div></div>") length strings we can pad the document with before IE fails to render in time
    N = kwargs.get("N", 1042)
    M = kwargs.get("M", 1000000)

    def child_count(n):
        if n > (N - math.log(M, 2)) - 1:
            # if n == N-1:
            #     return remaining_m_count
            # else:
            return 2
        else:
            return 1

    return TransformFunction("",
                              "move body content to the inside of a deeply nested tree of div elements",
                              mime_type_based_transform({
                                  'text/html': string_to_tfarg_function(lambda x : htmlmth.mods.html.move_body_to_nested_div_with_multiple_children(N, child_count, x))
                              }))

move_body_to_nested_div_with_children = _generate_move_body_to_nested_div_with_children()
move_body_to_nested_div_with_children.parameterize = _generate_move_body_to_nested_div_with_children
