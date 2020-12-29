import htmlmth.mods.http

from . import TransformFunction, http_payload_to_tfarg_function


encode_deflate_compression_none = TransformFunction("",
                                                  "deflate encoding (no compression)",
                                                  http_payload_to_tfarg_function(lambda x: htmlmth.mods.http.encode_deflate(x, compresslevel=0))
                                                  )

encode_deflate_compression_min = TransformFunction("",
                                                  "deflate encoding (min compression)",
                                                  http_payload_to_tfarg_function(lambda x: htmlmth.mods.http.encode_deflate(x, compresslevel=1))
                                                  )

encode_deflate_compression_max = TransformFunction("",
                                                  "deflate encoding (max compression)",
                                                  http_payload_to_tfarg_function(lambda x: htmlmth.mods.http.encode_deflate(x, compresslevel=9))
                                                  )

def _generate_encode_deflate_compression_some(*args, **kwargs):
    compresslevel = kwargs.get("compresslevel", 5)

    assert(1 < compresslevel < 9)

    return TransformFunction("",
                              "deflate encoding (some compression)",
                              http_payload_to_tfarg_function(lambda x: htmlmth.mods.http.encode_deflate(x, compresslevel=compresslevel))
                              )

encode_deflate_compression_some = _generate_encode_deflate_compression_some()
encode_deflate_compression_some.parameterize = _generate_encode_deflate_compression_some
