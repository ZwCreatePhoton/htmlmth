from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform
import htmlmth.mods.javascript


remove_comments = TransformFunction("",
                                         "remove JavaScript comments",
                                         mime_type_based_transform({
                                             'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.javascript.remove_comments(x)),
                                             'text/javascript': string_to_tfarg_function(lambda x: htmlmth.mods.javascript.remove_comments(x)),
                                         }))
