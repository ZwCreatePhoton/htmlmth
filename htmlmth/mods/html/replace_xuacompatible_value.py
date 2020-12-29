import re

from . import Mod


def replace_xuacompatible_value(value, output):
    p1 = re.compile('(?i)(<meta\s+http-equiv="x.*ua.*compatible".*content=")(.*)(".*>)')
    subst = r'''\1{0}\3'''.format(value)
    output = re.sub(p1, subst, output)

    p2 = re.compile('(?i)(<meta\s+content=")(.*)(".*http-equiv="x.*ua.*compatible".*>)')
    subst = r'''\1{0}\3'''.format(value)
    output = re.sub(p2, subst, output)

    return output

mod_replace_xuacompatible_value = Mod(replace_xuacompatible_value)
