def add_header(headers, name, value):
    header = "{}: {}".format(name, value)
    headers.append(header)
    return headers
