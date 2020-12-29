from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform
import htmlmth.mods.html


def _generate_move_body_to_nested_div(*args, **kwargs):
    N = kwargs.get("N", 1044)

    return TransformFunction("",
                                            "move body content to the inside of a deeply nested div element",
                                            mime_type_based_transform({
                                                'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.move_body_to_nested_div(N, x))
                                            }))


move_body_to_nested_div = _generate_move_body_to_nested_div()
move_body_to_nested_div.parameterize = _generate_move_body_to_nested_div
