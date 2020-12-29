from . import TransformFunction


_REASONS = {305: "Use Proxy",
            414: "Request-URI Too Large"}

def _set_status(tfargs, code, message):
    for tfarg in tfargs:
        tfarg.metadata.http.status_code = code
        tfarg.metadata.http.status_message = message
    return tfargs

def _generate_status_code_3xx(*args, **kwargs):
    statuscode = kwargs.get("statuscode", 300)
    statusmessage = _REASONS.get(statuscode, "Multiple Choices")

    assert(300 <= statuscode <= 399)

    return TransformFunction("",
                              "3XX status code ({})".format(statuscode),
                              lambda x: _set_status(x, statuscode, statusmessage)
                              )

status_code_3xx = _generate_status_code_3xx()
status_code_3xx.parameterize = _generate_status_code_3xx

def _generate_status_code_4xx(*args, **kwargs):
    statuscode = kwargs.get("statuscode", 400)
    statusmessage = _REASONS.get(statuscode, "Bad Request")

    assert(400 <= statuscode <= 499)

    return TransformFunction("",
                              "4XX status code ({})".format(statuscode),
                              lambda x: _set_status(x, statuscode, statusmessage)
                              )

status_code_4xx = _generate_status_code_4xx()
status_code_4xx.parameterize = _generate_status_code_4xx
