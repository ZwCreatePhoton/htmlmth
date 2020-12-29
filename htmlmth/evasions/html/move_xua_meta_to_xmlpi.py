from . import TransformFunction, mime_type_based_transform, string_to_tfarg_function
import htmlmth.mods.html


move_xua_meta_to_xmlpi = TransformFunction("",
                                        "remove x-ua-compatible meta element and replace with the x-ua-compatible Processing Instruction",
                                             mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(htmlmth.mods.html.move_xua_to_xmlpi)
                                        }))
