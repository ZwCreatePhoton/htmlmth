from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform
import htmlmth.mods.html


# data URLs for script tags (data_url_internal_script_*) requires IE 9+

data_url_internal_script_url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_data_no = TransformFunction("",
                                        "internal scripts changed to external scripts sourced from data urls (nonstandard base64 declaration, data base64 encoded)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.data_url_internal_script_url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_data_no(x))
                                        }))


data_url_internal_script_url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_data = TransformFunction("",
                                        "internal scripts changed to external scripts sourced from data urls (nonstandard base64 declaration, data base64 encoded, data percent encoded)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.data_url_internal_script_url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_data(x))
                                        }))


data_url_internal_script_url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_url = TransformFunction("",
                                        "internal scripts changed to external scripts sourced from data urls (nonstandard base64 declaration, data base64 encoded, url components percent encoded)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.data_url_internal_script_url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_url(x))
                                        }))


data_url_internal_script_url_gen_std_b64_declare_b64_encode_data_percent_encode_data_no = TransformFunction("",
                                        "internal scripts changed to external scripts sourced from data urls (standard base64 declaration, data base64 encoded)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.data_url_internal_script_url_gen_std_b64_declare_b64_encode_data_percent_encode_data_no(x))
                                        }))


data_url_internal_script_url_gen_std_b64_declare_b64_encode_data_percent_encode_data = TransformFunction("",
                                        "internal scripts changed to external scripts sourced from data urls (standard base64 declaration, data base64 encoded, data percent encoded)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.data_url_internal_script_url_gen_std_b64_declare_b64_encode_data_percent_encode_data(x))
                                        }))


data_url_internal_script_url_gen_std_b64_declare_b64_encode_data_percent_encode_url = TransformFunction("",
                                        "internal scripts changed to external scripts sourced from data urls (standard base64 declaration, data base64 encoded, url components percent encoded)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.data_url_internal_script_url_gen_std_b64_declare_b64_encode_data_percent_encode_url(x))
                                        }))


data_url_internal_script_url_gen_no_b64_declare_b64_encode_data_percent_encode_data_min = TransformFunction("",
                                        "internal scripts changed to external scripts sourced from data urls (no base64 declaration, data partially percent encoded)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.data_url_internal_script_url_gen_no_b64_declare_b64_encode_data_percent_encode_data_min(x))
                                        }))


data_url_internal_script_url_gen_no_b64_declare_b64_encode_data_percent_encode_data = TransformFunction("",
                                        "internal scripts changed to external scripts sourced from data urls (no base64 declaration, data percent encoded)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.data_url_internal_script_url_gen_no_b64_declare_b64_encode_data_percent_encode_data(x))
                                        }))


# TODO: more possible evasions with mime type, charset, BOM ?

