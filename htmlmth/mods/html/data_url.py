import re
from base64 import b64encode
from urllib import quote as urlencode


from . import Mod

TAG_NO_SRC_REGEX = r'(?i)(<TAGNAME)((?:(?!src=)[^>]*)>)((?:(?!<\/TAGNAME)[\w\W])*)(<\/TAGNAME>)' # g1=start of opening tag, g2=the rest of the opening tag, g3=the inner content of the tag, g4=the closing tag

def _urlencode_all(string):
    return "".join("%{0:0>2}".format(format(ord(char), "x")) for char in string)


_STANDARD_BASE64_DECLARATION = ";base64"
_NONSTANDARD_BASE64_DECLARATION = "; BaSe64     "
_NO_BASE64_DECLARATION = ""
_TRANSFER_ENCODE_AS_NONE = 1
_TRANSFER_ENCODE_AS_PERCENT = 2
_TRANSFER_ENCODE_AS_PERCENT_ALL = 3
_TRANSFER_ENCODE_AS_BASE64 = 4


## url generator functions

def _url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_data_no(data):
    url = "data:"
    url += _NONSTANDARD_BASE64_DECLARATION
    url += ","
    url += b64encode(data) # not going to encode '='
    return url

def _url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_data(data):
    url = "data:"
    url += _NONSTANDARD_BASE64_DECLARATION
    url += ","
    url += _urlencode_all(b64encode(data))
    return url

def _url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_url(data):
    url = "data:"
    url += _urlencode_all(_NONSTANDARD_BASE64_DECLARATION)
    url += ","
    url += _urlencode_all(b64encode(data))
    return url

def _url_gen_std_b64_declare_b64_encode_data_percent_encode_data_no(data):
    url = "data:"
    url += _STANDARD_BASE64_DECLARATION
    url += ","
    url += b64encode(data) # not going to encode '='
    return url

def _url_gen_std_b64_declare_b64_encode_data_percent_encode_data(data):
    url = "data:"
    url += _STANDARD_BASE64_DECLARATION
    url += ","
    url += _urlencode_all(b64encode(data))
    return url

def _url_gen_std_b64_declare_b64_encode_data_percent_encode_url(data):
    url = "data:"
    url += _urlencode_all(_STANDARD_BASE64_DECLARATION)
    url += ","
    url += _urlencode_all(b64encode(data))
    return url

def _url_gen_no_b64_declare_b64_encode_data_percent_encode_data_min(data):
    url = "data:"
    url += _NO_BASE64_DECLARATION
    url += ","
    url += urlencode(data)
    return url

def _url_gen_no_b64_declare_b64_encode_data_percent_encode_data(data):
    url = "data:"
    url += _NO_BASE64_DECLARATION
    url += ","
    url += _urlencode_all(data)
    return url

# # this would be equivlent to _url_gen_no_b64_declare_b64_encode_data_percent_encode_data
# def _url_gen_no_b64_declare_b64_encode_data_percent_encode_url(data):
#     pass

## end url generator functions


# internal tags (tag name = tagname) -> tags that point to a data url
def _data_url_internal_tag(output, url_gen, tagname, src_attribute_name="src"):
    pattern_tag = re.compile(TAG_NO_SRC_REGEX.replace("TAGNAME", tagname), )

    def replace_tag(m):
        opening_tag_start = m.group(1)
        opening_tag_end = m.group(2)
        tag_content = m.group(3)
        closing_tag_end = m.group(4)
        url = url_gen(tag_content)
        return opening_tag_start + ' {}="{}" '.format(src_attribute_name, url) + opening_tag_end + closing_tag_end

    output = pattern_tag.sub(replace_tag, output)
    return output


# internal script tags -> script tags that point to a data url
def _data_url_internal_script(output, url_gen):
    return _data_url_internal_tag(output, url_gen, "script")

def data_url_internal_script_url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_data_no(output):
    return _data_url_internal_script(output, _url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_data_no)

def data_url_internal_script_url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_data(output):
    return _data_url_internal_script(output, _url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_data)

def data_url_internal_script_url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_url(output):
    return _data_url_internal_script(output, _url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_url)

def data_url_internal_script_url_gen_std_b64_declare_b64_encode_data_percent_encode_data_no(output):
    return _data_url_internal_script(output, _url_gen_std_b64_declare_b64_encode_data_percent_encode_data_no)

def data_url_internal_script_url_gen_std_b64_declare_b64_encode_data_percent_encode_data(output):
    return _data_url_internal_script(output, _url_gen_std_b64_declare_b64_encode_data_percent_encode_data)

def data_url_internal_script_url_gen_std_b64_declare_b64_encode_data_percent_encode_url(output):
    return _data_url_internal_script(output, _url_gen_std_b64_declare_b64_encode_data_percent_encode_url)

def data_url_internal_script_url_gen_no_b64_declare_b64_encode_data_percent_encode_data_min(output):
    return _data_url_internal_script(output, _url_gen_no_b64_declare_b64_encode_data_percent_encode_data_min)

def data_url_internal_script_url_gen_no_b64_declare_b64_encode_data_percent_encode_data(output):
    return _data_url_internal_script(output, _url_gen_no_b64_declare_b64_encode_data_percent_encode_data)


mod_data_url_internal_script_url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_data_no = Mod(data_url_internal_script_url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_data_no)
mod_data_url_internal_script_url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_data = Mod(data_url_internal_script_url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_data)
mod_data_url_internal_script_url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_url = Mod(data_url_internal_script_url_gen_nonstd_b64_declare_b64_encode_data_percent_encode_url)
mod_data_url_internal_script_url_gen_std_b64_declare_b64_encode_data_percent_encode_data_no = Mod(data_url_internal_script_url_gen_std_b64_declare_b64_encode_data_percent_encode_data_no)
mod_data_url_internal_script_url_gen_std_b64_declare_b64_encode_data_percent_encode_data = Mod(data_url_internal_script_url_gen_std_b64_declare_b64_encode_data_percent_encode_data)
mod_data_url_internal_script_url_gen_std_b64_declare_b64_encode_data_percent_encode_url = Mod(data_url_internal_script_url_gen_std_b64_declare_b64_encode_data_percent_encode_url)
mod_data_url_internal_script_url_gen_no_b64_declare_b64_encode_data_percent_encode_data_min = Mod(data_url_internal_script_url_gen_no_b64_declare_b64_encode_data_percent_encode_data_min)
mod_data_url_internal_script_url_gen_no_b64_declare_b64_encode_data_percent_encode_data = Mod(data_url_internal_script_url_gen_no_b64_declare_b64_encode_data_percent_encode_data)
