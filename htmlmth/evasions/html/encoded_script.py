from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform
import htmlmth.mods.html


# requires IE mode <= 8
encoded_script = TransformFunction("",
                                     "encode vbscript/jscript (Scripting.Encoder)",
                                     mime_type_based_transform({
                                         'text/html': string_to_tfarg_function(lambda x : htmlmth.mods.html.encode_vbscript(encoded_script.SCRIPTING_ENCODER_SERVER, encoded_script.SCRIPTING_ENCODER_PORT, x))
                                     }),
                                     mime_type_based_transform({
                                         'text/html': string_to_tfarg_function(lambda x : htmlmth.mods.html.encode_javascript(encoded_script.SCRIPTING_ENCODER_SERVER, encoded_script.SCRIPTING_ENCODER_PORT, x))
                                     }),
                                   )
encoded_script.SCRIPTING_ENCODER_SERVER = None
encoded_script.SCRIPTING_ENCODER_PORT = None
