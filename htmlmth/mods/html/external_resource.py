import re

from . import Mod
from . import TransformFunctionArgument, MIME_TYPE_MAP, HttpMetaData

TAG_NO_SRC_REGEX = r'(?i)(<TAGNAME)((?:(?!src=)[^>]*)>)((?:(?!<\/TAGNAME)[\w\W])*)(<\/TAGNAME>)' # g1=start of opening tag, g2=the rest of the opening tag, g3=the inner content of the tag, g4=the closing tag


# internal tags (tag name = tagname) in a document (represented by tfarg) -> list of [document with tags that point to a data url, external resource 1, ... ]
def _external_resource_internal_tag(tfarg,  rel_path_gen, tagname, src_attribute_name="src"):
    pattern_tag = re.compile(TAG_NO_SRC_REGEX.replace("TAGNAME", tagname))

    external_resource_tfargs = []

    def create_external_resource_tfarg(content, path):
        file_ext = "." + path.split(".")[-1]
        tfa = TransformFunctionArgument(content=content, content_type=MIME_TYPE_MAP[file_ext])
        tfa.metadata.http.path = path
        return tfa

    def replace_tag(m):
        opening_tag_start = m.group(1)
        opening_tag_end = m.group(2)
        tag_content = m.group(3)
        closing_tag_end = m.group(4)
        rel_path = rel_path_gen(m)
        ext_resource_tfarg = create_external_resource_tfarg(tag_content, rel_path)
        HttpMetaData.copy_server_headers(tfarg.metadata.http, ext_resource_tfarg.metadata.http)
        external_resource_tfargs.append(ext_resource_tfarg)
        return opening_tag_start + ' {}="{}" '.format(src_attribute_name, rel_path) + opening_tag_end + closing_tag_end

    tfarg.content = pattern_tag.sub(replace_tag, tfarg.content)

    return [tfarg] + external_resource_tfargs


# internal script tags -> script tags that point to an external script url
def external_resource_internal_script(tfarg_list):
    if isinstance(tfarg_list, TransformFunctionArgument):
        tfarg_list = [tfarg_list]
    new_tfarg_list = []
    count = [0]
    def rel_path_gen(m):
        content = m.group(3)
        is_js = "jscript" in m.group().lower() or "javascript" in m.group().lower() or ";\n" in content
        file_ext = ".js" if is_js else ".vbs"
        rel_path = "/extscr{}{}".format(count[0], file_ext)
        count[0] += 1
        return rel_path
    for tfarg in tfarg_list:
        new_tfargs = _external_resource_internal_tag(tfarg, rel_path_gen, "script")
        new_tfarg_list += new_tfargs
    return new_tfarg_list

mod_external_resource_internal_script = Mod(external_resource_internal_script)
