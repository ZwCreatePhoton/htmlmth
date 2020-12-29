from . import TransformFunction, normalized_headers_to_tfarg_function
import htmlmth.mods.http


# todo: remove from .headers ?
def _remove_content_length_header(tfargs):
    for tfarg in tfargs:
        tfarg.metadata.http.content_length_header = None
    return tfargs

transferencoding_chunked = TransformFunction("",
                                             "Transfer-Encoding declared (chunked)",
                                             normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.add_header(x, "Transfer-Encoding", "chunked")),
                                             _remove_content_length_header
                                             )

transferencoding_gzip = TransformFunction("",
                                          "Transfer-Encoding declared (gzip)",
                                          normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.add_header(x, "Transfer-Encoding", "gzip")),
                                          _remove_content_length_header
                                          )

transferencoding_deflate = TransformFunction("",
                                             "Transfer-Encoding declared (deflate)",
                                             normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.add_header(x, "Transfer-Encoding", "deflate")),
                                             _remove_content_length_header
                                             )
