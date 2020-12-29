from base64 import b64encode

from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform
import htmlmth.mods.html


entity_encoding_attributes_dec = TransformFunction("",
                                        "encode attribute values (base 10)",
                                                   mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_attributes_dec(x))
                                        }))

entity_encoding_attributes_hex = TransformFunction("",
                                        "encode attribute values (base 16)",
                                                   mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_attributes_hex(x))
                                        }))

entity_encoding_attributes_mix = TransformFunction("",
                                        "encode attribute values (mixed base 10, base 16)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_attributes_mix(x))
                                        }))


# below are XML only

entity_encoding_attributes_internal_entity = TransformFunction("",
                                        "encode attribute values (single internal entity)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_attributes_internal_entity(x, "attributeentity"))
                                        }))

entity_encoding_attributes_internal_entities = TransformFunction("",
                                        "encode attribute values (many internal entities)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_attributes_internal_entities(x, _entity_name_func_b64))
                                        }))

entity_encoding_cdata_dec = TransformFunction("",
                                        "encode attribute values (base 10)",
                                                   mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_cdata_dec(x))
                                        }))

entity_encoding_cdata_hex = TransformFunction("",
                                        "encode cdata sections (base 16)",
                                                   mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_cdata_hex(x))
                                        }))

entity_encoding_cdata_mix = TransformFunction("",
                                        "encode cdata sections (mixed base 10, base 16)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_cdata_mix(x))
                                        }))

entity_encoding_cdata_cdata = TransformFunction("",
                                        "encode cdata sections (chunk into many cdata sections)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_cdata_cdata(x))
                                        }))


entity_encoding_cdata_internal_entity = TransformFunction("",
                                        "encode cdata sections (single internal entity)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_cdata_internal_entity(x, "cdataentity"))
                                        }))

# u_ord should be the unicode ordinal to a character in the set: NameStartChar https://www.w3.org/TR/REC-xml/#NT-NameStartChar
def _entity_name_func_single_uchr(u_ord):
    def g(u):
        prefix = ""
        name = prefix
        name += unichr(u_ord).encode('utf_8') * u
        return name
    return g

def _entity_name_func_b64(u):
    prefix = "_"
    name = prefix
    name += b64encode(unichr(u)).replace('=', '').replace('+', '-').replace('/', '.')
    return name


entity_encoding_cdata_internal_entities = TransformFunction("",
                                        "encode cdata sections (many internal entities)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_cdata_internal_entities(x, _entity_name_func_b64))
                                        }))



entity_encoding_root_internal_entity = TransformFunction("",
                                        "encode root element text (single internal entity)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_root_internal_entity(x, "rootentity"))
                                        }))

# if there are no (general) entities declared, then this will not do anything. So should be combined with another evasion
entity_encoding_internal_entity_declaration_dec = TransformFunction("",
                                        "encode internal entity declarations (base 10)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_internal_entity_declaration_dec(x))
                                        }))

# if there are no (general) entities declared, then this will not do anything. So should be combined with another evasion
entity_encoding_internal_entity_declaration_hex = TransformFunction("",
                                        "encode internal entity declarations (base 16)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_internal_entity_declaration_hex(x))
                                        }))

# if there are no (general) entities declared, then this will not do anything. So should be combined with another evasion
entity_encoding_internal_entity_declaration_mix = TransformFunction("",
                                        "encode internal entity declarations (mixed base 10, base 16)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_internal_entity_declaration_mix(x))
                                        }))


# Parameters: min_value_length
def _generate_entity_encoding_internal_entity_declaration_internal_parameter_entity(*args, **kwargs):
    min_value_length = kwargs.get("min_value_length", 0)
    return TransformFunction(   "",
                                "encode " + ("some " if min_value_length > 0 else "") + "internal entity declarations (single internal parameter entity)",
                                mime_type_based_transform({
                                'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_internal_entity_declaration_internal_parameter_entity(x, min_value_length))
                                }))
# if there are no (general) entities declared, then this will not do anything. So should be combined with another evasion
entity_encoding_internal_entity_declaration_internal_parameter_entity = _generate_entity_encoding_internal_entity_declaration_internal_parameter_entity(min_value_length=0)
entity_encoding_internal_entity_declaration_internal_parameter_entity.parameterize = _generate_entity_encoding_internal_entity_declaration_internal_parameter_entity


def _generate_entity_encoding_internal_parameter_entity_declaration_nested_internal_parameter_entities(*args, **kwargs):
    number_of_nested = kwargs.get("number_of_nested", 30000)
    prepend_junk_entity_def = kwargs.get("prepend_junk_entity_def", False)
    return TransformFunction(   "",
                                "encode internal parameter entity declarations (many nested internal parameter entities)",
                                mime_type_based_transform({
                                    'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_internal_parameter_entity_declaration_nested_internal_parameter_entities(x, number_of_nested, prepend_junk_entity_def=prepend_junk_entity_def))
                                }))


# if there are no parameter entities declared, then this will not do anything. So should be combined with another evasion
entity_encoding_internal_parameter_entity_declaration_nested_internal_parameter_entities = _generate_entity_encoding_internal_parameter_entity_declaration_nested_internal_parameter_entities(number_of_nested=30000, prepend_junk_entity_def=False)
entity_encoding_internal_parameter_entity_declaration_nested_internal_parameter_entities.parameterize = _generate_entity_encoding_internal_parameter_entity_declaration_nested_internal_parameter_entities



# if there are no parameter entities declared, then this will not do anything. So should be combined with another evasion
entity_encoding_internal_parameter_entity_declaration_dec = TransformFunction("",
                                        "encode internal parameter entity declarations (base 10)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_internal_parameter_entity_declaration_dec(x))
                                        }))

# if there are no parameter entities declared, then this will not do anything. So should be combined with another evasion
entity_encoding_internal_parameter_entity_declaration_hex = TransformFunction("",
                                        "encode internal parameter entity declarations (base 16)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_internal_parameter_entity_declaration_hex(x))
                                        }))

# if there are no parameter entities declared, then this will not do anything. So should be combined with another evasion
entity_encoding_internal_parameter_entity_declaration_mix = TransformFunction("",
                                        "encode internal parameter entity declarations (mixed base 10, base 16)",
                                        mime_type_based_transform({
                                            'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.entity_encoding_internal_parameter_entity_declaration_mix(x))
                                        }))


# todo: insertion of undefined entities references to break regexes

# todo: encode all leaf tags' contents
