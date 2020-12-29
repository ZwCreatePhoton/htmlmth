from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform
import htmlmth.mods.html


insert_slash_after_opening_tag_names = TransformFunction("",
                                                         'insert "/" after opening tag names',
                                                         mime_type_based_transform({
                                                             'text/html': string_to_tfarg_function(lambda x : htmlmth.mods.html.insert_slash_after_opening_tag_names(x, 1))
                                                         }))
