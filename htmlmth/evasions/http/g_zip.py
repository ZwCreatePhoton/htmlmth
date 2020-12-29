import htmlmth.mods.http

from . import TransformFunction, http_payload_to_tfarg_function
import htmlmth.mods.http


encode_gzip_compression_none = TransformFunction("",
                                                  "gzip encoding (no compression)",
                                                  http_payload_to_tfarg_function(lambda x: htmlmth.mods.http.encode_gzip(x, compresslevel=0))
                                                  )

encode_gzip_compression_min = TransformFunction("",
                                                  "gzip encoding (min compression)",
                                                  http_payload_to_tfarg_function(lambda x: htmlmth.mods.http.encode_gzip(x, compresslevel=1))
                                                  )

encode_gzip_compression_max = TransformFunction("",
                                                  "gzip encoding (max compression)",
                                                  http_payload_to_tfarg_function(lambda x: htmlmth.mods.http.encode_gzip(x, compresslevel=9))
                                                  )

def _generate_encode_gzip_compression_some(*args, **kwargs):
    compresslevel = kwargs.get("compresslevel", 5)

    assert(1 < compresslevel < 9)

    return TransformFunction("",
                              "gzip encoding (some compression)",
                              http_payload_to_tfarg_function(lambda x: htmlmth.mods.http.encode_gzip(x, compresslevel=compresslevel))
                              )

encode_gzip_compression_some = _generate_encode_gzip_compression_some()
encode_gzip_compression_some.parameterize = _generate_encode_gzip_compression_some
