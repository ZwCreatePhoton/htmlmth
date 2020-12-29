from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform
import htmlmth.mods.html


encoded_vbscript = TransformFunction("",
                                     "encode vbscript",
                                     mime_type_based_transform({
                                         'text/html': string_to_tfarg_function(lambda x : htmlmth.mods.html.encode_vbscript(encoded_vbscript.SCRIPTING_ENCODER_SERVER, encoded_vbscript.SCRIPTING_ENCODER_PORT, x))
                                     }))
encoded_vbscript.SCRIPTING_ENCODER_SERVER = None
encoded_vbscript.SCRIPTING_ENCODER_PORT = None
