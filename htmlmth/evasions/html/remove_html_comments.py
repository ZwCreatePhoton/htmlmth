from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform
import htmlmth.mods.html


remove_html_comments = TransformFunction("",
                                         "remove html comments",
                                         mime_type_based_transform({
                                             'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.remove_html_comments(x))
                                         }))
