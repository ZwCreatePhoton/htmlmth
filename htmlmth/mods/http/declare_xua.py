import re


def _is_xuacompatible_header(header):
    return "x-ua-compatible" in header.lower()


def _replace_xua(ie_version, header):
    header = header.split(":")[0] + ": " + ie_version
    return header


def declare_xua(ie_version, headers):
    has_xuacompatible_header = False
    for i in range(len(headers)):
        header = headers[i]
        if _is_xuacompatible_header(header):
            has_xuacompatible_header = True
            header = _replace_xua(ie_version, header)
        headers[i] = header
    if not has_xuacompatible_header:
        headers.append("x-ua-compatible: {}".format(ie_version))
    return headers
