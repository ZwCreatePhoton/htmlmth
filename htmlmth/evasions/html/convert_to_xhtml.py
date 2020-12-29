from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform, normalized_headers_to_tfarg_function
import htmlmth.mods.html
import htmlmth.mods.http
from ..html import xua_move_meta_to_xmlpi

# TODO: remove use of  and add note that .encode should not be present before using

## Note:
# Probably won't work if exploit requires document mode <= 8

# might chane back to xuacompatible in http headers for xml docs


# TODO: convert metadata mimetype to xhtml

#
_convert_to_xhtml = TransformFunction("",
                                        "convert to XHTML document with an xml declaration tag",
                                      mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.convert_to_xhtml(x))
                                        })
                                      )

_convert_to_xhtml_no_xml_tag = TransformFunction("",
                                        "convert to XHTML document with no declaration xml tag",
                                                 mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.convert_to_xhtml(x, xml_decl=False))
                                        }),
                                                 )

#https://docs.microsoft.com/en-us/openspecs/ie_standards/ms-iedoco/638b52a6-c5a1-433d-b872-ca07b8f06bdd
# IE will use the XML parser when the above content-types are declared



# IE will parse with HTML parser
convert_to_xhtml_no_xml_tag_http_declared_no_type = TransformFunction("",
                                                                      _convert_to_xhtml_no_xml_tag.description + " ;" + "no declared MIME type in http headers",
                                                                      _convert_to_xhtml_no_xml_tag,
                                                                      mime_type_based_transform({
                                                               'text/html': normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.remove_header("Content-Type", x))
                                                             }),
                                                                      )

# soft assumption: text/xml declared in document
convert_to_xhtml_no_xml_tag_http_declared_no_type_inferred_xml = TransformFunction("",
                                                                                   _convert_to_xhtml_no_xml_tag.description + " ;" + "no declared MIME type in http headers" + " ;" + xua_move_meta_to_xmlpi.description,
                                                                                   _convert_to_xhtml_no_xml_tag,
                                                                      mime_type_based_transform({
                                                               'text/html': normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.remove_header("Content-Type", x))
                                                             }),
                                                                                   xua_move_meta_to_xmlpi,
                                                                                   # x-ua-compatible http-equiv meta tags do not get interpreted with IE's XML parser
                                                                                   

                                                                                   )



# IE will parse with HTML parser
convert_to_xhtml_no_xml_tag_http_declared_text_html = TransformFunction("",
                                                                        _convert_to_xhtml_no_xml_tag.description + " ;" + "declared as text/html in http headers",
                                                                        _convert_to_xhtml_no_xml_tag,
                                                                        mime_type_based_transform({
                                                                 'text/html': normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.declare_mime_type("text/html", x))
                                                             }),
                                                                        )

# this one might not work?
# soft assumption: text/xml declared in document
convert_to_xhtml_no_xml_tag_http_declared_text_html_inferred_xml = TransformFunction("",
                                                                                     _convert_to_xhtml_no_xml_tag.description + " ;" + "declared as text/html in http headers" + " ;" + xua_move_meta_to_xmlpi.description,
                                                                                     _convert_to_xhtml_no_xml_tag,
                                                                        mime_type_based_transform({
                                                                 'text/html': normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.declare_mime_type("text/html", x))
                                                             }),
                                                                        xua_move_meta_to_xmlpi,
                                                                        # x-ua-compatible http-equiv meta tags do not get interpreted with IE's XML parser
                                                                        

                                                                        )
# IE will parse with XML parser
convert_to_xhtml_no_xml_tag_http_declared_text_xml = TransformFunction("",
                                                                       _convert_to_xhtml_no_xml_tag.description + " ;" + "declared as text/xml in http headers" + " ;" + xua_move_meta_to_xmlpi.description,
                                                                       _convert_to_xhtml_no_xml_tag,
                                                                       mime_type_based_transform({
                                                                'text/html': normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.declare_mime_type("text/xml", x))
                                                            }),
                                                                       xua_move_meta_to_xmlpi,
                                                                       # x-ua-compatible http-equiv meta tags do not get interpreted with IE's XML parser
                                                                       

                                                                       )

# IE will parse with XML parser
convert_to_xhtml_no_xml_tag_http_declared_application_xml = TransformFunction("",
                                                                              _convert_to_xhtml_no_xml_tag.description + " ;" + "declared as application/xml in http headers" + " ;" + xua_move_meta_to_xmlpi.description,
                                                                              _convert_to_xhtml_no_xml_tag,
                                                                              mime_type_based_transform({
                                                               'text/html': normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.declare_mime_type("application/xml", x))
                                                           }),
                                                                              xua_move_meta_to_xmlpi ,  # x-ua-compatible http-equiv meta tags do not get interpreted with IE's XML parser
                                                                              
                                                                              )

# IE will parse with XML parser
convert_to_xhtml_no_xml_tag_http_declared_application_xhtml_xml = TransformFunction("",
                                                                                    _convert_to_xhtml_no_xml_tag.description + " ;" + "declared as application/xhtml+xml in http headers" + " ;" + xua_move_meta_to_xmlpi.description,
                                                                                    _convert_to_xhtml_no_xml_tag,
                                                                                    mime_type_based_transform({
                                                                 'text/html': normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.declare_mime_type("application/xhtml+xml", x))
                                                             }),
                                                                                    xua_move_meta_to_xmlpi ,  # x-ua-compatible http-equiv meta tags do not get interpreted with IE's XML parser
                                                                              
                                                                                    )

# IE will parse with XML parser
convert_to_xhtml_no_xml_tag_http_declared_image_svg_xml = TransformFunction("",
                                                                            _convert_to_xhtml_no_xml_tag.description + " ;" + "declared as image/svg+xml in http headers" + " ;" + xua_move_meta_to_xmlpi.description,
                                                                            _convert_to_xhtml_no_xml_tag,
                                                                            mime_type_based_transform({
                                                                 'text/html': normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.declare_mime_type("image/svg+xml", x))
                                                             }),
                                                                            xua_move_meta_to_xmlpi ,  # x-ua-compatible http-equiv meta tags do not get interpreted with IE's XML parser
                                                                              
                                                                            )


# the output of convert_to_xhtml will begin with the <?xml ...?> tag (technically an optional x(ht)ml tag in some cases). When a document begins with that tag, IE will use its XML parser instead of HTML parser, even if you specifiy the mime type as "text/html" if it cant infer its mime type from other information

# IE will parse with HTML parser if "text/html" content-type http-equiv meta tag is in the document
# Otherwise, IE will parse with XML parser
# Soft assumption: document does not contain "text/html" content-type http-equiv meta tag
# OR http path for file ends with ".xml" (needs confirmation)
convert_to_xhtml_http_declared_no_type = TransformFunction("",
                                                           _convert_to_xhtml.description + " ;" + "no declared MIME type in http headers" + " ;" + xua_move_meta_to_xmlpi.description,
                                                           _convert_to_xhtml,
                                                           mime_type_based_transform({
                                                               'text/html': normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.remove_header("Content-Type", x))
                                                             }),
                                                           xua_move_meta_to_xmlpi ,  # x-ua-compatible http-equiv meta tags do not get interpreted with IE's XML parser
                                                                              
                                                           )

# soft assumption: document contains "text/html" content-type http-equiv meta tag
# OR http path for file ends with ".html"/".htm" (needs confirmation)
convert_to_xhtml_http_declared_no_type_inferred_html = TransformFunction("",
                                                           _convert_to_xhtml.description + " ;" + "no declared MIME type in http headers",
                                                           _convert_to_xhtml,
                                                           mime_type_based_transform({
                                                               'text/html': normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.remove_header("Content-Type", x))
                                                             }),
                                                           )


# IE will parse with HTML parser if "text/html" content-type http-equiv meta tag is in the document
# Otherwise, IE will parse with XML parser
# Soft assumption: document does not contain "text/html" content-type http-equiv meta tag
# OR http path for file ends with ".xml" (needs confirmation)
convert_to_xhtml_http_declared_text_html = TransformFunction("",
                                                             _convert_to_xhtml.description + " ;" + "declared as text/html in http headers" + " ;" + xua_move_meta_to_xmlpi.description,
                                                             _convert_to_xhtml,
                                                             mime_type_based_transform({
                                                                 'text/html': normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.declare_mime_type("text/html", x))
                                                             }),
                                                             xua_move_meta_to_xmlpi ,  # x-ua-compatible http-equiv meta tags do not get interpreted with IE's XML parser
                                                                              
                                                             )

# soft assumption: document contains "text/html" content-type http-equiv meta tag
# OR http path for file ends with ".html"/".htm" (needs confirmation)
convert_to_xhtml_http_declared_text_html_inferred_html = TransformFunction("",
                                                             _convert_to_xhtml.description + " ;" + "declared as text/html in http headers",
                                                             _convert_to_xhtml,
                                                             mime_type_based_transform({
                                                                 'text/html': normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.declare_mime_type("text/html", x))
                                                             }),
                                                             )


# IE will parse with XML parser
convert_to_xhtml_http_declared_text_xml = TransformFunction("",
                                                            _convert_to_xhtml.description + " ;" + "declared as text/xml in http headers" + " ;" + xua_move_meta_to_xmlpi.description,
                                                            _convert_to_xhtml,
                                                            mime_type_based_transform({
                                                                'text/html': normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.declare_mime_type("text/xml", x))
                                                            }),
                                                            xua_move_meta_to_xmlpi ,  # x-ua-compatible http-equiv meta tags do not get interpreted with IE's XML parser
                                                                              
                                                            )

# IE will parse with XML parser
convert_to_xhtml_http_declared_application_xml = TransformFunction("",
                                                                   _convert_to_xhtml.description + " ;" + "declared as application/xml in http headers" + " ;" + xua_move_meta_to_xmlpi.description,
                                                                   _convert_to_xhtml,
                                                                   mime_type_based_transform({
                                                               'text/html': normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.declare_mime_type("application/xml", x))
                                                           }),
                                                                   xua_move_meta_to_xmlpi ,  # x-ua-compatible http-equiv meta tags do not get interpreted with IE's XML parser
                                                                              
                                                                   )

# IE will parse with XML parser
convert_to_xhtml_http_declared_application_xhtml_xml = TransformFunction("",
                                                                         _convert_to_xhtml.description + " ;" + "declared as application/xhtml+xml in http headers" + " ;" + xua_move_meta_to_xmlpi.description,
                                                                         _convert_to_xhtml,
                                                                         mime_type_based_transform({
                                                                 'text/html': normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.declare_mime_type("application/xhtml+xml", x))
                                                             }),
                                                                         xua_move_meta_to_xmlpi ,  # x-ua-compatible http-equiv meta tags do not get interpreted with IE's XML parser
                                                                              
                                                                         )

# IE will parse with XML parser
convert_to_xhtml_http_declared_image_svg_xml = TransformFunction("",
                                                                 _convert_to_xhtml.description + " ;" + "declared as image/svg+xml in http headers" + " ;" + xua_move_meta_to_xmlpi.description,
                                                                 _convert_to_xhtml,
                                                                 mime_type_based_transform({
                                                                 'text/html': normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.declare_mime_type("image/svg+xml", x))
                                                             }),
                                                                 xua_move_meta_to_xmlpi ,  # x-ua-compatible http-equiv meta tags do not get interpreted with IE's XML parser
                                                                              
                                                                 )

# IE will parse with XML parser
convert_to_xhtml_http_declared_image_gif = TransformFunction("",
                                                             _convert_to_xhtml.description + " ;" + "declared as image/gif in http headers" + " ;" + xua_move_meta_to_xmlpi.description,
                                                             _convert_to_xhtml,
                                                             mime_type_based_transform({
                                                                 'text/html': normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.declare_mime_type("image/gif", x))
                                                             }),
                                                             xua_move_meta_to_xmlpi ,  # x-ua-compatible http-equiv meta tags do not get interpreted with IE's XML parser
                                                                              
                                                             )
# IE will parse with HTML parser if "text/html" content-type http-equiv meta tag is in the document
# Otherwise, IE will parse with XML parser
# Soft assumption: document does not contain "text/html" content-type http-equiv meta tag
# OR http path for file ends with ".xml" (needs confirmation)
# soft assumption: document contains "text/html" content-type http-equiv meta tag
# OR http path for file ends with ".html"/".htm" (needs confirmation)
convert_to_xhtml_http_declared_image_gif_inferred_html = TransformFunction("",
                                                             _convert_to_xhtml.description + " ;" + "declared as image/gif in http headers",
                                                             _convert_to_xhtml,
                                                             mime_type_based_transform({
                                                                 'text/html': normalized_headers_to_tfarg_function(lambda x: htmlmth.mods.http.declare_mime_type("image/gif", x))
                                                             }),
                                                             )
