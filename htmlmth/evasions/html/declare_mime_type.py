from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform
import htmlmth.mods.html


meta_declared_text_html = TransformFunction("",
                                        "declared as text/html in a meta http-equiv tag",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.declare_mime_type("text/html", x))
                                        }))

meta_declared_text_xml = TransformFunction("",
                                        "declared as text/xml in a meta http-equiv tag",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.declare_mime_type("text/xml", x))
                                        }))
