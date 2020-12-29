from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform
import htmlmth.mods.html


remove_content_type_http_equiv_meta = TransformFunction("",
                                         "remove meta http-equiv content-type declaration",
                                         mime_type_based_transform({
                                             'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.remove_html_tag_meta_http_equiv("content-type", x))
                                         }))
