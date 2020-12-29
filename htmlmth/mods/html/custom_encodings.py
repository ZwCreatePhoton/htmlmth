import binascii

def utf_8(ustring):
    return ustring.encode("utf_8")

# Only for BMP characters
# For non-BMP characters this might be useful
# https://en.wikipedia.org/wiki/Plane_(Unicode)
# https://stackoverflow.com/questions/40222971/python-find-equivalent-surrogate-pair-from-non-bmp-unicode-char
def utf_16_be(ustring):
    return ustring.encode("utf_16_be")

# see note above
def utf_16_le(ustring):
    return ustring.encode("utf_16_le")


_UTF_7_SET_D = {u"",
                u"A",
                u"B",
                u"C",
                u"D",
                u"E",
                u"F",
                u"G",
                u"H",
                u"I",
                u"J",
                u"K",
                u"L",
                u"M",
                u"N",
                u"O",
                u"P",
                u"Q",
                u"R",
                u"S",
                u"T",
                u"U",
                u"V",
                u"W",
                u"X",
                u"Y",
                u"Z",
                u"a",
                u"b",
                u"c",
                u"d",
                u"e",
                u"f",
                u"g",
                u"h",
                u"i",
                u"j",
                u"k",
                u"l",
                u"m",
                u"n",
                u"o",
                u"p",
                u"q",
                u"r",
                u"s",
                u"t",
                u"u",
                u"v",
                u"w",
                u"x",
                u"y",
                u"z",
                u"0",
                u"1",
                u"2",
                u"3",
                u"4",
                u"5",
                u"6",
                u"7",
                u"8",
                u"9",
                u"'",
                u"(",
                u")",
                u",",
                u"-",
                u".",
                u"/",
                u":",
                u"?"}

_UTF_7_SET_O = {u"!",
                u'"',
                u"#",
                u"$",
                u"%",
                u"&",
                u"*",
                u";",
                u"<",
                u"=",
                u">",
                u"@",
                u"[",
                u"]",
                u"^",
                u"_",
                u"'",
                u"{",
                u"|",
                u"}"}

_UTF_7_SET_RULE3 = {unichr(32), # space
                    unichr(9), # tab
                    unichr(13), # carriage return
                    unichr(10)} # line feed


def _modified_base64(s):
    # TODO: support non-BMP characters
    s = s.encode('utf-16be')
    return binascii.b2a_base64(s).rstrip('\n=')

def _doB64(_in, r, individual=False):
    if _in:
        if individual:
            for i in _in:
                r.append('+{}-'.format(_modified_base64(i)))
        else:
            r.append('+{}-'.format(_modified_base64(''.join(_in))))
        del _in[:]

def _utf_7(ustring, direct_set, individual=False):
    r = []
    _in = []
    for c in ustring:
        if c in direct_set:
            _doB64(_in, r, individual)
            r.append(c)
        elif c == '+':
            _doB64(_in, r, individual)
            r.append('+-')
        else:
            _in.append(c)
    _doB64(_in, r, individual)
    return str(''.join(r))


# direct set = _UTF_7_SET_D + a subset of _UTF_7_SET_O + _UTF_7_SET_RULE3
def utf_7_0(ustring):
    return ustring.encode("utf_7")

def utf_7_1(ustring):
    direct_set = _UTF_7_SET_D | _UTF_7_SET_O | _UTF_7_SET_RULE3
    return _utf_7(ustring, direct_set)

def utf_7_2(ustring):
    direct_set = _UTF_7_SET_D | _UTF_7_SET_RULE3
    return _utf_7(ustring, direct_set)

def utf_7_3(ustring):
    direct_set = _UTF_7_SET_D | _UTF_7_SET_O
    return _utf_7(ustring, direct_set)

def utf_7_4(ustring):
    direct_set = _UTF_7_SET_O | _UTF_7_SET_RULE3
    return _utf_7(ustring, direct_set)

def utf_7_5(ustring):
    direct_set = {}
    return _utf_7(ustring, direct_set)

# direct_set = {} ; modified b64 operates on individual characters instead on consecutive characters
def utf_7_5_i(ustring):
    direct_set = {}
    return _utf_7(ustring, direct_set, True)
