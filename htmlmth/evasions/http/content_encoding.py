from . import TransformFunction, normalized_headers_to_tfarg_function
import htmlmth.mods.http


contentencoding_gzip = TransformFunction("",
                                             "Content-Encoding declared (gzip)",
                                             normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.add_header(x, "Content-Encoding", "gzip"))
                                             )

contentencoding_deflate = TransformFunction("",
                                             "Content-Encoding declared (deflate)",
                                             normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.add_header(x, "Content-Encoding", "deflate"))
                                             )
