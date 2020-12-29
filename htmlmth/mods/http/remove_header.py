

def _is_header(header_to_remove, header):
    return header_to_remove.lower() in header.split(":")[0].lower()


def remove_header(header_to_remove, headers):
    header_indexes = []
    for i in range(len(headers)):
        header = headers[i]
        if _is_header(header_to_remove, header):
            header_indexes.append(i)
    for i in reversed(header_indexes):
        del headers[i]
    return headers
