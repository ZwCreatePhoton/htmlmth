import htmlmth.mods.http

from . import TransformFunction, http_payload_to_tfarg_function


def _generate_encode_chunked_equisize(*args, **kwargs):
    chunksize = kwargs.get("chunksize", 256)

    assert(chunksize > 0)

    return TransformFunction("",
                              "chunked encoding (equisize)",
                              http_payload_to_tfarg_function(lambda x: htmlmth.mods.http.encode_chunked_equisize(x, chunksize=chunksize))
                              )

encode_chunked_equisize = _generate_encode_chunked_equisize()
encode_chunked_equisize.parameterize = _generate_encode_chunked_equisize

def _generate_encode_chunked_equisize_leadingzeros(*args, **kwargs):
    chunksize = kwargs.get("chunksize", 256)
    leadingzeros = kwargs.get("leadingzeros", 10)

    assert(chunksize > 0)
    assert(leadingzeros > 1)

    return TransformFunction("",
                              "chunked encoding (equisize, chunk sizes with leading zeros)",
                              http_payload_to_tfarg_function(lambda x: htmlmth.mods.http.encode_chunked_equisize(x, chunksize=chunksize, leadingzeros=leadingzeros))
                              )

encode_chunked_equisize_leadingzeros = _generate_encode_chunked_equisize_leadingzeros()
encode_chunked_equisize_leadingzeros.parameterize = _generate_encode_chunked_equisize_leadingzeros

def _generate_encode_chunked_varysize(*args, **kwargs):
    min_chunksize = kwargs.get("min_chunksize", 128)
    max_chunksize = kwargs.get("max_chunksize", 256)

    assert(min_chunksize > 0)
    assert(max_chunksize > 0)
    assert(min_chunksize < max_chunksize)

    return TransformFunction("",
                              "chunked encoding (various sizes)",
                              http_payload_to_tfarg_function(lambda x: htmlmth.mods.http.encode_chunked_varysize(x, min_chunksize=min_chunksize, max_chunksize=max_chunksize))
                              )

encode_chunked_varysize = _generate_encode_chunked_varysize()
encode_chunked_varysize.parameterize = _generate_encode_chunked_varysize

def _generate_encode_chunked_equisize_leadingzeros(*args, **kwargs):
    min_chunksize = kwargs.get("min_chunksize", 128)
    max_chunksize = kwargs.get("max_chunksize", 256)
    leadingzeros = kwargs.get("leadingzeros", 10)

    assert (min_chunksize > 0)
    assert (max_chunksize > 0)
    assert (min_chunksize < max_chunksize)
    assert(leadingzeros > 1)

    return TransformFunction("",
                             "chunked encoding (various sizes, chunk sizes with leading zeros)",
                             http_payload_to_tfarg_function(
                                 lambda x: htmlmth.mods.http.encode_chunked_varysize(x, min_chunksize=min_chunksize,
                                                                             max_chunksize=max_chunksize, leadingzeros=leadingzeros))
                             )

encode_chunked_varysize_leadingzeros = _generate_encode_chunked_equisize_leadingzeros()
encode_chunked_varysize_leadingzeros.parameterize = _generate_encode_chunked_equisize_leadingzeros
