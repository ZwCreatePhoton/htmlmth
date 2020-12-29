import re


def _is_content_type_header(header):
    return "content-type" in header.lower()


def _has_encoding_set(header):
    return "charset" in header


def _replace_encoding(encoding, header):
    p1 = re.compile(r"(?i)(charset=)(.+)(.*)")
    header = p1.sub(lambda m: m.group(1) + encoding + m.group(2), header)
    return header


def declare_encoding(encoding, headers):
    has_content_type_header = False
    for i in range(len(headers)):
        header = headers[i]
        if _is_content_type_header(header):
            has_content_type_header = True
            if _has_encoding_set(header):
                header = _replace_encoding(encoding, header)
            else:
                header += "; charset={}".format(encoding)
        headers[i] = header
    if not has_content_type_header:
        headers.append("Content-Type: ; charset={}".format(encoding))
    return headers