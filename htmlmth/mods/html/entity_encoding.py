import re

from . import Mod


HTML_TAG_REGEX = r"<(\w+\b[^<>]*)>"
HTML_TAG_ATTR_VALUE_REGEX_dq = r'"([^"]*)"'
HTML_TAG_ATTR_VALUE_REGEX_sq = r"'([^']*)'"

# group 2 i the cdata section
XML_CDATA_SECTION_REGEX = r"(<!\[CDATA\[)((?:(?!\]\]>)[\w\W])*)(\]\]>)"
XML_ROOT_CONTENT_REGEX = r"(<html[^>]*>)([\w\W]*)(<\/html>)"


def _alternating_funcs(*args):
    count = [0]
    def g(x):
        count[0] += 1
        f = args[count[0] % len(args)]
        return f(x)
    return g


def _entity_encode_base_10(u):
    return "&#" + str(u) + ";"


def _entity_encode_base_16(u):
    return "&#x" + hex(u)[2:] + ";"


def _entity_encode_string(s, encoding_func):
    if "&#" in s:  # at least 1 character is already entity encoded ; want to avoid acidently double entity encoding
        return s
    characters = list(s)
    for i in range(len(characters)):
        characters[i] = encoding_func(ord(characters[i]))
    return "".join(characters)


def _entity_encoding_attributes(funcs, output):
    p1 = re.compile(HTML_TAG_REGEX)
    p2 = re.compile(HTML_TAG_ATTR_VALUE_REGEX_dq)
    p3 = re.compile(HTML_TAG_ATTR_VALUE_REGEX_sq)

    def replace_attr_value(attr_value):
        return _entity_encode_string(attr_value, _alternating_funcs(*funcs))

    def replace_tag_content(tag_content):
        # entity encoding x-ua-compatible will break the document
        if "x-ua-compatible" in tag_content.lower():
            return tag_content
        tag_content = p2.sub(lambda m: '"' + replace_attr_value(m.group(1)) + '"', tag_content)
        tag_content = p3.sub(lambda m: "'" + replace_attr_value(m.group(1)) + "'", tag_content)
        return tag_content

    output = p1.sub(lambda m: replace_tag_content(m.group()), output)
    return output


def entity_encoding_attributes_hex(output):
    return _entity_encoding_attributes([_entity_encode_base_16], output)

def entity_encoding_attributes_dec(output):
    return _entity_encoding_attributes([_entity_encode_base_10], output)

def entity_encoding_attributes_mix(output):
    return _entity_encoding_attributes([_entity_encode_base_10, _entity_encode_base_16], output)

def entity_encoding_attributes_internal_entity(output, entity_basename):
    p1 = re.compile(HTML_TAG_REGEX)
    p2 = re.compile(HTML_TAG_ATTR_VALUE_REGEX_dq)
    p3 = re.compile(HTML_TAG_ATTR_VALUE_REGEX_sq)

    custom_entities = {}
    count = [0]
    def replace_attr_value(old_content):
        entity_name = entity_basename + str(count[0])
        entity_value = _xml_entity_escape(old_content)
        custom_entities[entity_name] = entity_value
        new_content = "&" + entity_name + ";"
        count[0] = count[0] + 1
        return new_content

    def replace_tag_content(tag_content):
        # entity encoding x-ua-compatible will break the document
        if "x-ua-compatible" in tag_content.lower():
            return tag_content
        tag_content = p2.sub(lambda m: '"' + replace_attr_value(m.group(1)) + '"', tag_content)
        tag_content = p3.sub(lambda m: "'" + replace_attr_value(m.group(1)) + "'", tag_content)
        return tag_content

    output = p1.sub(lambda m: replace_tag_content(m.group()), output)

    for custom_entity_name in custom_entities:
        custom_entity_value = custom_entities[custom_entity_name]
        entity_declartion = '<!ENTITY ' + custom_entity_name + ' "' + custom_entity_value + '">'
        output = _insert_internal_dtd_line(output, entity_declartion)

    return output

# entity_name_gen_func(unicode_number) -> entity name
def entity_encoding_attributes_internal_entities(output, entity_name_gen_func):
    p1 = re.compile(HTML_TAG_REGEX)
    p2 = re.compile(HTML_TAG_ATTR_VALUE_REGEX_dq)
    p3 = re.compile(HTML_TAG_ATTR_VALUE_REGEX_sq)

    custom_entities = {}
    def replace_attr_value(old_content):
        new_content = ""
        for c in old_content:
            entity_name = entity_name_gen_func(ord(c))
            entity_value = _xml_entity_escape(c)
            custom_entities[entity_name] = entity_value
            new_content += "&" + entity_name + ";"
        return new_content

    def replace_tag_content(tag_content):
        # entity encoding x-ua-compatible will break the document
        if "x-ua-compatible" in tag_content.lower():
            return tag_content
        tag_content = p2.sub(lambda m: '"' + replace_attr_value(m.group(1)) + '"', tag_content)
        tag_content = p3.sub(lambda m: "'" + replace_attr_value(m.group(1)) + "'", tag_content)
        return tag_content

    output = p1.sub(lambda m: replace_tag_content(m.group()), output)

    for custom_entity_name in custom_entities:
        custom_entity_value = custom_entities[custom_entity_name]
        entity_declartion = '<!ENTITY ' + custom_entity_name + ' "' + custom_entity_value + '">'
        output = _insert_internal_dtd_line(output, entity_declartion)

    return output


mod_entity_encoding_attributes_hex = Mod(entity_encoding_attributes_hex)
mod_entity_encoding_attributes_dec = Mod(entity_encoding_attributes_dec)
mod_entity_encoding_attributes_mix = Mod(entity_encoding_attributes_mix)
mod_entity_encoding_attributes_internal_entity = Mod(entity_encoding_attributes_internal_entity)
mod_entity_encoding_attributes_internal_entities = Mod(entity_encoding_attributes_internal_entities)


# The below are for XML only

# references counted as 1 character
def _character_count(s):
    count = 0
    i = 0
    while i < len(s):
        if s[i] == '&':
            while s[i] != ';':
                i += 1
        count += 1
        i += 1
    return count

def _insert_internal_dtd_line(output, line, append=True):
    p1 = re.compile(r'(<!DOCTYPE[^<>\[\]]*")>') # regex for DOCTYPE tag without internal DTD declaration
    internal_dtd_skeleton = "[\n]"
    # if DOCTYPE tag doesnt have an internal DTD declaration yet (p1 matches), then insert an empty one
    output = p1.sub(lambda m: m.group(1) + " " + internal_dtd_skeleton + ">", output)

    p2 = re.compile(r'(<!DOCTYPE[^\[<]*)\[((?:(?!\n\]>)[\w\W])*)\n\]>') # regex for DOCTYPE tag with internal DTD declaration: group#1 is everything before the opening of the DTD declaration ("[") ; group#2 is the DTD content
    if line not in output:
        if append:
            output = p2.sub(lambda m: m.group(1) + "[" + ('\n' if m.group(2) and m.group(2)[0] != '\n' else '') + m.group(2) + '\n' + line + "\n]>", output)
        else:
            output = p2.sub(lambda m: m.group(1) + "[\n" + line + ('\n' if m.group(2) and m.group(2)[0] != '\n' else '') + m.group(2) + "\n]>", output)
    return output

def _xml_entity_escape(output, characters = ["&", '"', "'", "<", ">", "%"], replace_map = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        "<": "&lt;",
        ">": "&gt;",
        "%": "&#37;",
    }):
    for c in characters:
        if c in replace_map:
            output = output.replace(c, replace_map[c])
    return output

def _entity_encode_cdata(u):
    return "<![CDATA[" + unichr(u) + "]]>"

def _entity_encoding_cdata(funcs, output):
    p1 = re.compile(XML_CDATA_SECTION_REGEX)

    def replace_cdata_content(m):
        old_content = m.group(2)
        new_content = _entity_encode_string(old_content, _alternating_funcs(*funcs))
        return new_content

    output = p1.sub(lambda m: replace_cdata_content(m), output)
    return output

def entity_encoding_cdata_hex(output):
    return _entity_encoding_cdata([_entity_encode_base_16], output)

def entity_encoding_cdata_dec(output):
    return _entity_encoding_cdata([_entity_encode_base_10], output)

def entity_encoding_cdata_mix(output):
    return _entity_encoding_cdata([_entity_encode_base_10, _entity_encode_base_16], output)

def entity_encoding_cdata_cdata(output):
    return _entity_encoding_cdata([_entity_encode_cdata], output)

# cdata sections will be defined in a single internal entity
def entity_encoding_cdata_internal_entity(output, entity_basename):
    p1 = re.compile(XML_CDATA_SECTION_REGEX)

    custom_entities = {}
    count = [0]
    def replace_cdata_content(m):
        entity_name = entity_basename + str(count[0])
        old_content = m.group(2)
        entity_value = _xml_entity_escape(old_content)
        custom_entities[entity_name] = entity_value
        new_content = "&" + entity_name + ";"
        count[0] = count[0] + 1
        return new_content

    output = p1.sub(lambda m: replace_cdata_content(m), output)

    for custom_entity_name in custom_entities:
        custom_entity_value = custom_entities[custom_entity_name]
        entity_declartion = '<!ENTITY ' + custom_entity_name + ' "' + custom_entity_value + '">'
        output = _insert_internal_dtd_line(output, entity_declartion)

    return output

# cdata sections will be defined in terms of internal entities (1 character = 1 internal entity)
# entity_name_gen_func(unicode_number) -> entity name
def entity_encoding_cdata_internal_entities(output, entity_name_gen_func):
    p1 = re.compile(XML_CDATA_SECTION_REGEX)

    custom_entities = {}
    def replace_cdata_content(m):
        old_content = m.group(2)
        new_content = ""
        for c in old_content:
            entity_name = entity_name_gen_func(ord(c))
            entity_value = _xml_entity_escape(c)
            custom_entities[entity_name] = entity_value
            new_content += "&" + entity_name + ";"
        return new_content

    output = p1.sub(lambda m: replace_cdata_content(m), output)

    for custom_entity_name in custom_entities:
        custom_entity_value = custom_entities[custom_entity_name]
        entity_declartion = '<!ENTITY ' + custom_entity_name + ' "' + custom_entity_value + '">'
        output = _insert_internal_dtd_line(output, entity_declartion)

    return output

mod_entity_encoding_cdata_hex = Mod(entity_encoding_cdata_hex)
mod_entity_encoding_cdata_dec = Mod(entity_encoding_cdata_dec)
mod_entity_encoding_cdata_mix = Mod(entity_encoding_cdata_mix)
mod_entity_encoding_cdata_cdata = Mod(entity_encoding_cdata_cdata)
mod_entity_encoding_cdata_internal_entity = Mod(entity_encoding_cdata_internal_entity)
mod_entity_encoding_cdata_internal_entities = Mod(entity_encoding_cdata_internal_entities)


# the content of the root element (root assumed to be "html") will be defined in a single internal entity
def entity_encoding_root_internal_entity(output, entity_basename):
    root_node_name = re.compile(r'<!DOCTYPE (\w+)').search(output).group(1)
    p1 = re.compile(XML_ROOT_CONTENT_REGEX.replace("html", root_node_name))

    custom_entities = {}
    count = [0]
    def replace_root_content(m):
        entity_name = entity_basename + str(count[0])
        old_content = m.group(2)
        entity_value = _xml_entity_escape(old_content, characters=['&', '%', '"'], replace_map={'&':"&#38;", '%':"&#37;", '"':"&#34;"})
        custom_entities[entity_name] = entity_value
        new_content = "&" + entity_name + ";"
        count[0] = count[0] + 1
        return m.group(1) + new_content + m.group(3)

    output = p1.sub(lambda m: replace_root_content(m), output)

    for custom_entity_name in custom_entities:
        custom_entity_value = custom_entities[custom_entity_name]
        entity_declartion = '<!ENTITY ' + custom_entity_name + ' "' + custom_entity_value + '">'
        output = _insert_internal_dtd_line(output, entity_declartion)

    return output

# the mod that would be "entity_encoding_root_internal_entities" doesn't work

mod_entity_encoding_root_internal_entity = Mod(entity_encoding_root_internal_entity)


# encoding of 'entity encoding declaration' via a parameter entity
def entity_encoding_internal_entity_declaration_internal_parameter_entity(output, min_value_length=0):
    pattern_dtd = re.compile(r'(<!DOCTYPE[^\[<]*)\[((?:(?!\n\]>)[\w\W])*)\n\]>') # regex for DOCTYPE tag with internal DTD declaration: group#1 is everything before the opening of the DTD declaration ("[") ; group#2 is the DTD content
    pattern_entity_declaration_dq = re.compile(r'(<!ENTITY )([\w]+)( ")([^"]*)(">)')
    pattern_entity_declaration_sq = re.compile(r"(<!ENTITY )([\w]+)( ')([^']*)('>)")

    def replace_entity_declaration(m, escape_char):
        entity_declaration_name = m.group(2)
        entity_declaration_value = m.group(4)
        if _character_count(entity_declaration_value) < min_value_length: # dont act on entity declarations with values less than min_value_length characters
            return m.group()
        escaped_entity_declaration_value = _xml_entity_escape(entity_declaration_value, characters=['&'], replace_map={'&':'&#38;'})
        escaped_entity_declaration = m.group(1) +\
                                     m.group(2) +\
                                     _xml_entity_escape(m.group(3), characters=[escape_char], replace_map={escape_char:'&#{};'.format(ord(escape_char))}) +\
                                     escaped_entity_declaration_value + \
                                     _xml_entity_escape(m.group(5), characters=[escape_char], replace_map={escape_char:'&#{};'.format(ord(escape_char))})
        parameter_entity_declaration_name = "p" + entity_declaration_name
        parameter_entity_declaration = "<!ENTITY % " + parameter_entity_declaration_name + " " + '"' + escaped_entity_declaration + '">'
        return parameter_entity_declaration + "\n" + "%{};".format(parameter_entity_declaration_name)

    def replace_dtd(m):
        old_content = m.group(2)
        new_content = old_content
        new_content = pattern_entity_declaration_dq.sub(lambda x: replace_entity_declaration(x, '"'), new_content)
        new_content = pattern_entity_declaration_sq.sub(lambda x: replace_entity_declaration(x, "'"), new_content)
        return m.group(1) + "[" + new_content + "\n]>"

    output = pattern_dtd.sub(replace_dtd, output)
    return output

mod_entity_encoding_internal_entity_declaration_internal_parameter_entity = Mod(entity_encoding_internal_entity_declaration_internal_parameter_entity)

# encoding of 'parameter entity encoding declaration' via nested (N >= 1) parameter entities
def entity_encoding_internal_parameter_entity_declaration_nested_internal_parameter_entities(output, N, prepend_junk_entity_def=False):
    assert(N >= 1)
    pattern_dtd = re.compile(r'(<!DOCTYPE[^\[<]*)\[((?:(?!\n\]>)[\w\W])*)\n\]>') # regex for DOCTYPE tag with internal DTD declaration: group#1 is everything before the opening of the DTD declaration ("[") ; group#2 is the DTD content
    pattern_entity_declaration_dq = re.compile(r'(<!ENTITY % )([\w]+)( ")([^"]*)(">)')
    pattern_entity_declaration_sq = re.compile(r"(<!ENTITY % )([\w]+)( ')([^']*)('>)")

    def replace_parameter_entity_declaration(m, escape_char):
        new_declarations = []
        base_parameter_entity_declaration_name = m.group(2)
        base_parameter_entity_declaration_value = m.group(4)
        last_parameter_entity_declaration_name = base_parameter_entity_declaration_name + str(N)
        last_parameter_entity_declaration =   m.group(1) + \
                                    last_parameter_entity_declaration_name +\
                                    m.group(3) + \
                                    base_parameter_entity_declaration_value +\
                                    m.group(5)
        new_declarations.append(last_parameter_entity_declaration)
        for n in reversed(range(N)):
            parameter_entity_name = base_parameter_entity_declaration_name
            parameter_entity_value = "&#37;{};".format(parameter_entity_name + str(n+1))
            if n != 0:
                parameter_entity_name += str(n)
            parameter_entity_declaration = m.group(1) + parameter_entity_name + m.group(3) + parameter_entity_value + m.group(5)
            new_declarations.append(parameter_entity_declaration)
        return "\n".join(new_declarations)

    def replace_dtd(m):
        old_content = m.group(2)
        new_content = old_content
        new_content = pattern_entity_declaration_dq.sub(lambda x: replace_parameter_entity_declaration(x, '"'), new_content)
        new_content = pattern_entity_declaration_sq.sub(lambda x: replace_parameter_entity_declaration(x, "'"), new_content)
        return m.group(1) + "[" + new_content + "\n]>"

    output = pattern_dtd.sub(replace_dtd, output)

    JUNK_ENTITY_DEF = '<!ENTITY junk "abcd">'
    if prepend_junk_entity_def:
        output = _insert_internal_dtd_line(output, JUNK_ENTITY_DEF, append=False)

    return output

mod_entity_encoding_internal_parameter_entity_declaration_nested_internal_parameter_entities = Mod(entity_encoding_internal_parameter_entity_declaration_nested_internal_parameter_entities)


# (general) entity values will be defined in terms of character references hex/dec/mix
def _entity_encoding_internal_entity_declaration(funcs, output):
    pattern_dtd = re.compile(
        r'(<!DOCTYPE[^\[<]*)\[((?:(?!\n\]>)[\w\W])*)\n\]>')  # regex for DOCTYPE tag with internal DTD declaration: group#1 is everything before the opening of the DTD declaration ("[") ; group#2 is the DTD content
    pattern_entity_declaration_dq = re.compile(r'(<!ENTITY )([\w]+)( ")([^"]*)(">)')
    pattern_entity_declaration_sq = re.compile(r"(<!ENTITY )([\w]+)( ')([^']*)('>)")


    f = _alternating_funcs(*funcs)
    def replace_value(value):
        return _entity_encode_string(value, f)

    def replace_parameter_entity_declaration(m, escape_char):
        old_content = m.group(4)
        new_content = ""
        i = 0
        while i < len(old_content):
            # assume that all '&' are a part of a character / entity reference
            if old_content[i] == '&':
                while old_content[i] != ';':
                    new_content += old_content[i]
                    i += 1
                new_content += old_content[i]
                i += 1
                continue
            c = old_content[i]
            new_content += replace_value(c)
            i += 1
        return m.group(1) + m.group(2) + m.group(3) + new_content + m.group(5)

    def replace_dtd(m):
        old_content = m.group(2)
        new_content = old_content
        new_content = pattern_entity_declaration_dq.sub(lambda x: replace_parameter_entity_declaration(x, '"'),
                                                        new_content)
        new_content = pattern_entity_declaration_sq.sub(lambda x: replace_parameter_entity_declaration(x, "'"),
                                                        new_content)
        return m.group(1) + "[" + new_content + "\n]>"

    output = pattern_dtd.sub(replace_dtd, output)

    return output

def entity_encoding_internal_entity_declaration_hex(output):
    return _entity_encoding_internal_entity_declaration([_entity_encode_base_16], output)

def entity_encoding_internal_entity_declaration_dec(output):
    return _entity_encoding_internal_entity_declaration([_entity_encode_base_10], output)

def entity_encoding_internal_entity_declaration_mix(output):
    return _entity_encoding_internal_entity_declaration([_entity_encode_base_16, _entity_encode_base_10], output)


mod_entity_encoding_internal_entity_declaration_hex = Mod(entity_encoding_internal_entity_declaration_hex)
mod_entity_encoding_internal_entity_declaration_dec = Mod(entity_encoding_internal_entity_declaration_dec)
mod_entity_encoding_internal_entity_declaration_mix = Mod(entity_encoding_internal_entity_declaration_mix)

# parameter entity values will be defined in terms of character references hex/dec/mix
def _entity_encoding_internal_parameter_entity_declaration(funcs, output):
    pattern_dtd = re.compile(
        r'(<!DOCTYPE[^\[<]*)\[((?:(?!\n\]>)[\w\W])*)\n\]>')  # regex for DOCTYPE tag with internal DTD declaration: group#1 is everything before the opening of the DTD declaration ("[") ; group#2 is the DTD content
    pattern_entity_declaration_dq = re.compile(r'(<!ENTITY % )([\w]+)( ")([^"]*)(">)')
    pattern_entity_declaration_sq = re.compile(r"(<!ENTITY % )([\w]+)( ')([^']*)('>)")


    f = _alternating_funcs(*funcs)
    def replace_value(value):
        return _entity_encode_string(value, f)

    def replace_parameter_entity_declaration(m, escape_char):
        old_content = m.group(4)
        new_content = ""
        i = 0
        while i < len(old_content):
            # assume that all '&' are a part of a character / entity reference
            if old_content[i] == '&':
                while old_content[i] != ';':
                    new_content += old_content[i]
                    i += 1
                new_content += old_content[i]
                i += 1
                continue
            c = old_content[i]
            new_content += replace_value(c)
            i += 1
        return m.group(1) + m.group(2) + m.group(3) + new_content + m.group(5)

    def replace_dtd(m):
        old_content = m.group(2)
        new_content = old_content
        new_content = pattern_entity_declaration_dq.sub(lambda x: replace_parameter_entity_declaration(x, '"'),
                                                        new_content)
        new_content = pattern_entity_declaration_sq.sub(lambda x: replace_parameter_entity_declaration(x, "'"),
                                                        new_content)
        return m.group(1) + "[" + new_content + "\n]>"

    output = pattern_dtd.sub(replace_dtd, output)

    return output

def entity_encoding_internal_parameter_entity_declaration_hex(output):
    return _entity_encoding_internal_parameter_entity_declaration([_entity_encode_base_16], output)

def entity_encoding_internal_parameter_entity_declaration_dec(output):
    return _entity_encoding_internal_parameter_entity_declaration([_entity_encode_base_10], output)

def entity_encoding_internal_parameter_entity_declaration_mix(output):
    return _entity_encoding_internal_parameter_entity_declaration([_entity_encode_base_16, _entity_encode_base_10], output)


mod_entity_encoding_internal_parameter_entity_declaration_hex = Mod(entity_encoding_internal_parameter_entity_declaration_hex)
mod_entity_encoding_internal_parameter_entity_declaration_dec = Mod(entity_encoding_internal_parameter_entity_declaration_dec)
mod_entity_encoding_internal_parameter_entity_declaration_mix = Mod(entity_encoding_internal_parameter_entity_declaration_mix)