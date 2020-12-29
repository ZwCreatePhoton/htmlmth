from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform
import htmlmth.mods.html


# TODO: script decoding
# so for now there's a soft assumption: the script in "javascript.encode"/"vbscript.ecode" code blocks are not encoded
remove_script_encoding = TransformFunction("",
                                         'encoded javascript/vbscript decoded and langauge declarations changed to "javascript"/"vbscript"',
                                         mime_type_based_transform({
                                             'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.set_javascript_tag_language("javascript", x) if "javascript.encode" in x.lower() else x)
                                         }),
                                         mime_type_based_transform({
                                             'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.set_vbscript_tag_language("vbscript", x) if "vbscript.encode" in x.lower() else x)
                                         }),
                                           )
