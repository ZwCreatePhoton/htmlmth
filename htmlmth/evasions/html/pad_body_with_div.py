from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform
import htmlmth.mods.html


def _generate_pad_body_with_div(*args, **kwargs):
    N = kwargs.get("N", 1000000)
    return TransformFunction("",
                              "pad the body with many div elements",
                              mime_type_based_transform({
                                  'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.prepend_content_into_body("<div></div>"*N, x))
                              }))


pad_body_with_div = _generate_pad_body_with_div()
pad_body_with_div.parameterize = _generate_pad_body_with_div
