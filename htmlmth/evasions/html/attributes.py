from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform
import htmlmth.mods.html


attributes_reverse = TransformFunction("",
                                         "reverse the order of attributes",
                                         mime_type_based_transform({
                                             'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.attributes_reverse(x))
                                         }))

attributes_insert_newlines = TransformFunction("",
                                         "insert newlines into attribute values",
                                         mime_type_based_transform({
                                             'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.attributes_insert_newline(x, every_n=1, multiplier=1))
                                         }))


def _generate_attributes_insert_many_newlines(*args, **kwargs):
    every_n = kwargs.get("every_n", 1)
    multiplier = kwargs.get("multiplier", 10)
    assert(multiplier > 1)
    return TransformFunction("",
                            "insert sequences of newlines into attribute values",
                            mime_type_based_transform({
                                'text/html': string_to_tfarg_function(
                                    lambda x: htmlmth.mods.html.attributes_insert_newline(x,
                                                                                  every_n=every_n,
                                                                                  multiplier=multiplier))
                            }))

attributes_insert_many_newlines = _generate_attributes_insert_many_newlines()
attributes_insert_many_newlines.parameterize = _generate_attributes_insert_many_newlines
