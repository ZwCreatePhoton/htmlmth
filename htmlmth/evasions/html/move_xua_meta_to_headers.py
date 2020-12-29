from . import TransformFunction, mime_type_based_transform
import htmlmth.mods.html


def _move_xua_meta_to_headers(tfarg):
    output = tfarg.content
    headers = tfarg.metadata.http.normalized_headers
    output, headers = htmlmth.mods.html.move_xua_to_headers(output, headers)
    tfarg.content = output
    tfarg.metadata.http.normalized_headers = headers
    return tfarg

move_xua_meta_to_headers = TransformFunction("",
                                        "remove x-ua-compatible meta element and send x-ua-compatible as an HTTP header instead",
                                             mime_type_based_transform({
                                            'text/html': _move_xua_meta_to_headers
                                        }))
