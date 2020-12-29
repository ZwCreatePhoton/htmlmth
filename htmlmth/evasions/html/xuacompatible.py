from . import TransformFunction, mime_type_based_transform, string_to_tfarg_function
import htmlmth.mods.html


def _move_xua_meta_to_headers(tfarg):
    output = tfarg.content
    headers = tfarg.metadata.http.normalized_headers
    output, headers = htmlmth.mods.html.move_xua_to_headers(output, headers)
    tfarg.content = output
    tfarg.metadata.http.normalized_headers = headers
    return tfarg

xua_move_meta_to_headers = TransformFunction("",
                                        "remove x-ua-compatible meta element and send x-ua-compatible as an HTTP header instead",
                                             mime_type_based_transform({
                                            'text/html': _move_xua_meta_to_headers
                                        }))

xua_move_meta_to_xmlpi = TransformFunction("",
                                        "remove x-ua-compatible meta element and replace with the x-ua-compatible Processing Instruction",
                                           mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(htmlmth.mods.html.move_xua_to_xmlpi)
                                        }))

xua_meta_change_value_8 = TransformFunction("",
                                        "change x-ua-compatible meta element value (IE=8)",
                                             mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x : htmlmth.mods.html.replace_xuacompatible_value("IE=8", x))
                                        }))

xua_meta_change_value_9 = TransformFunction("",
                                        "change x-ua-compatible meta element value (IE=9)",
                                             mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x : htmlmth.mods.html.replace_xuacompatible_value("IE=9", x))
                                        }))

xua_meta_change_value_10 = TransformFunction("",
                                        "change x-ua-compatible meta element value (IE=10)",
                                             mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x : htmlmth.mods.html.replace_xuacompatible_value("IE=10", x))
                                        }))
