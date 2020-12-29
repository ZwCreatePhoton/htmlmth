import re

from . import Mod


def declare_xua_xmlpi(value, output):
    p = re.compile('(<meta\s+http-equiv="x.*ua.*compatible".*content=")(.*)(".*>)')
    subst = r'''\1{0}\3'''.format(value)
    output = re.sub(p, subst, output)
    return output

mod_declare_xua_xmlpi = Mod(declare_xua_xmlpi)
