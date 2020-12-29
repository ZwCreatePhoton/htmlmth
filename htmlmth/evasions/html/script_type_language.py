from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform
import htmlmth.mods.html


script_language_remove_encode = TransformFunction("",
                                         'script language declarations changed from jscript.encode/vbscript.encode',
                                         mime_type_based_transform({
                                             'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.set_javascript_tag_language("javascript", x) if "jscript.encode" in x.lower() else x)
                                         }),
                                         mime_type_based_transform({
                                             'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.set_vbscript_tag_language("vbscript", x) if "vbscript.encode" in x.lower() else x)
                                         }),
                                           )

script_language_add_encode = TransformFunction("",
                                         'script language declarations changed to jscript.encode/vbscript.encode ;script type declarations removed',
                                         mime_type_based_transform({
                                             'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.set_javascript_tag_language("jscript.encode", x) if "jscript.encode" not in x.lower() else x)
                                         }),
                                         mime_type_based_transform({
                                             'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.set_vbscript_tag_language("vbscript.encode", x) if "vbscript.encode" not in x.lower() else x)
                                         }),
                                               mime_type_based_transform({
                                                   'text/html': string_to_tfarg_function(
                                                       lambda x: htmlmth.mods.html.remove_script_tag_type(x))
                                               }),
                                           )
