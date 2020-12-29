import re


def _is_content_type_header(header):
    return "content-type" in header.lower()


def _has_mime_type_set(header):
    return header.split(":")[1].split(";")[0].strip() != ""


def _replace_mime_type(mime_type, header):
    p1 = re.compile(r"(:\s*)([^;]+)(;*)")
    header = p1.sub(lambda m: m.group(1) + mime_type + m.group(3), header)
    return header


def declare_mime_type(mime_type, headers):
    has_content_type_header = False
    for i in range(len(headers)):
        header = headers[i]
        if _is_content_type_header(header):
            has_content_type_header = True
            if _has_mime_type_set(header):
                header = _replace_mime_type(mime_type, header)
            else:
                header = header.split(":")[0] + ":" + mime_type + header.split(":")[1]
        headers[i] = header
    if not has_content_type_header:
        headers.append("Content-Type: {}".format(mime_type))
    return headers