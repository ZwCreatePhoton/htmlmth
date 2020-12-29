from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform
import htmlmth.mods.html


reverse_attributes = TransformFunction("",
                                         "reverse the order of attributes",
                                         mime_type_based_transform({
                                             'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.attributes_reverse(x))
                                         }))
