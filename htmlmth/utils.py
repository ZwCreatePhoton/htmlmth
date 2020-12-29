import os

import yaml

from HTMLScriptExtractor import HTMLScriptExtractor


MIME_TYPE_MAP = {
    '.htm': 'text/html',
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.vbs': 'text/vbscript',
    '.txt': 'text/plain',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg'
}


# input:
#   a function "mime_type_function_dict" a dictionary (mime type -> f) where "f" is a function that accepts the tuple: (string, MetaData) and returns the tuple: (string, MetaData)
# output:
#   a function "g" that accepts a single argument of type list of tuple: (string, MetaData)
#       # in this function, for each tuple in the list, the function mime_type_function_dict[tuple[1].mime_type] will be called with tuple as the argument
def mime_type_based_transform(mime_type_function_dict):
    def g(list_of_tfarg):
        new_list_of_tfarg = []
        for tfarg in list_of_tfarg:
            f = mime_type_function_dict.get(tfarg.metadata.mime_type, None)
            ret = None
            if callable(f):
                ret = f(tfarg)
            if isinstance(ret, TransformFunctionArgument):
                new_list_of_tfarg.append(tfarg)
            elif isinstance(ret, list):
                new_list_of_tfarg += ret
            else:
                new_list_of_tfarg.append(tfarg)
        return new_list_of_tfarg
    return g


# for use with TransformFunctionArgument.content
# function(string) -> function(TransformFunctionArgument)
def string_to_tfarg_function(f):
    def g(tfarg):
        tfarg.content = f(tfarg.content)
        return tfarg
    return g


# for use with TransformFunctionArgument.metadata.http.normalized_headers
# function(list of headers) -> function(TransformFunctionArgument)
def normalized_headers_to_tfarg_function(f):
    def g(tfarg):
        is_list = isinstance(tfarg, list)
        tfargs = tfarg if is_list else [tfarg]
        for tfa in tfargs:
            tfa.metadata.http.normalized_headers = f(tfa.metadata.http.normalized_headers)
        if is_list:
            return tfargs
        else:
            return tfarg
    return g

# for use with TransformFunctionArgument.metadata.http.payload
# function(bytes) -> function(TransformFunctionArgument)
def http_payload_to_tfarg_function(f):
    def g(tfarg):
        is_list = isinstance(tfarg, list)
        tfargs = tfarg if is_list else [tfarg]
        for tfa in tfargs:
            tfa.metadata.http.body = f(tfa.metadata.http.body)
        if is_list:
            return tfargs
        else:
            return tfarg
    return g


def replace_apply_replace_back(f, s, sub):
    def g(input):
        output = input.replace(s, sub)
        output = f(output)
        output = output.replace(sub, s)
        return output
    return g


class TransformFunction():
    def __init__(self, name=None, description=None, *args):
        self._name = name
        self._description = description
        self._functions = args
        self.parameters = {}

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        if self._description:
            return self._description
        else:
            return "; ".join(f.description for f in self._functions)

    def __call__(self, *args, **kwargs):
        ret = args[0]
        for func in self._functions:
            ret = func(ret)
        return ret

    def parameterize(self, **kwargs):
        raise NotImplemented

    @staticmethod
    # clean up the descriptions of all TransformFunction objects in "transform_functions" using the name and description propteries of TransformFunction objects with an index < "index"
    def cleanup_descriptions(transform_functions, index=0):
        for j in reversed(range(len(transform_functions))):
            test_case = transform_functions[j]
            description = test_case.description
            pieces = set(description.split("; "))
            used_pieces = set()
            new_descriptions = []
            for i in range(index):
                if i == j:
                    continue
                tc = transform_functions[i]
                tc_description = tc.description
                tc_pieces = set(tc_description.split("; "))
                has_all_pieces = all(p in pieces for p in tc_pieces)
                if has_all_pieces:
                    used_pieces.update(tc_pieces)
                    new_descriptions.append(tc.name)
            missing_pieces = pieces - used_pieces
            test_case._description = "; ".join(new_descriptions + list(missing_pieces))


class TransformFunctionArgument():
    def __init__(self, content=None, content_type=None):
        self.content = content
        self.metadata = MetaData(data=self, mime_type=content_type)

    def __str__(self):
        return self.content

    def __len__(self):
        return len(str(self))


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class MetaData():
    def __init__(self, data, mime_type=None):
        self.data = data
        self.mime_type = mime_type
        self.http = HttpMetaData(data, mime_type=mime_type)


class HttpMetaData():
    NEWLINE = "\r\n"

    def __init__(self, data, type="response", version="1.1", mime_type=None, content_length_header=True, content_type_header=False, server_header=False, connection_header=False):
        self._body = None
        self.data = data
        self.type = type
        self.host = ""
        self.path = "/"
        self.is_launch_path = False
        self.version = version
        self.status_code = 200
        self.status_message = "OK"
        self.mime_type = mime_type if mime_type is not None else "text/html"
        self._headers = None
        self._normalized_headers = None
        self.server_header = server_header
        self.server_header_value = ""
        self.content_type_header = content_type_header
        self.connection_header = connection_header
        self.connection_header_value = "close"
        self.content_length_header = content_length_header

    @property
    def normalized_headers(self):
        if self._normalized_headers is None:
            self._normalized_headers = []
            if self.server_header:
                h = "Server: {}".format(self.server_header_value)
                self._normalized_headers.append(h)
            if self.content_type_header:
                h = "Content-Type: {}".format(self.mime_type)
                self._normalized_headers.append(h)
            if self.connection_header:
                h = "Connection: {}".format(self.connection_header_value)
                self._normalized_headers.append(h)
        return self._normalized_headers

    @normalized_headers.setter
    def normalized_headers(self, normalized_headers):
        self._normalized_headers = normalized_headers

    @property
    def headers(self):
        if self._headers:
            return self._headers
        else:
            headers_bytes = ""
            if self.type == "response":
                headers_bytes += "HTTP/{} {} {}".format(self.version, self.status_code, self.status_message) + HttpMetaData.NEWLINE
            else:
                pass # TODO
            # Assumption: the "headers" property will only be called after modifications to the payload are complete
            #   -> content-length will not be updated after accessing this property for the first time
            self.normalized_headers
            if self.content_length_header:
                h = "Content-Length: {}".format(len(self.body))
                self._normalized_headers.append(h)
            for h in self._normalized_headers:
                headers_bytes += h + HttpMetaData.NEWLINE
            headers_bytes += HttpMetaData.NEWLINE
            self._headers = headers_bytes
            return self._headers

    @headers.setter
    def headers(self, headers):
        self._headers = headers

    # normalized body: before chunking, compression, etc.
    @property
    def payload(self):
        return self.data.content

    # raw body: after chunking, compression, etc.
    @property
    def body(self):
        if self._body is None:
            return self.payload
        else:
            return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @staticmethod
    def copy_server_headers(input_hmd, output_hmd):
        output_hmd.server_header = input_hmd.server_header
        output_hmd.server_header_value = input_hmd.server_header_value
        output_hmd.content_type_header = input_hmd.content_type_header
        output_hmd.content_length_header = input_hmd.content_length_header
        output_hmd.connection_header = input_hmd.connection_header


def IsYaml(filepath):
    return os.path.splitext(filepath)[-1].lower() == ".yaml"


# returns list of baseline
# baseline := dictionary of "host", "path", "filepath", "content"
def ParseBaselineYaml(filepath):
    filepath = os.path.normpath(filepath.replace("\\", "/")) # normalize
    baselines = []
    with open(filepath) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        if "include" in data:
            for include_yaml in data["include"]:
                baselines.extend(ParseBaselineYaml(os.path.join(os.path.abspath(os.path.dirname(filepath)), include_yaml)))
        else:
            if data['baselines'] is None:
                return baselines
            for baseline in data['baselines']:
                normalized_filepath = os.path.normpath(baseline["filepath"].replace("\\", "/"))
                bl = {
                    "host": baseline["host"] if "host" in baseline else "",
                    "path": baseline["path"] if "path" in baseline else normalized_filepath.replace("\\", "/"),
                    "filepath": normalized_filepath,
                    "content": open(os.path.join(os.path.abspath(os.path.dirname(filepath)), normalized_filepath), "r").read(),
                }
                if bl["path"][0] != "/":
                    bl["path"] = "/" + bl["path"]
                baselines.append(bl)
    return baselines


# returns list of testcase
# testcase := dictionary of "host", "path", "casename"
def ParseTestcaseYaml(filepath):
    filepath = os.path.normpath(filepath.replace("\\", "/")) # normalize
    baselines = []
    with open(filepath) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        if data is None:
            return baselines
        if "include" in data:
            for include_yaml in data["include"]:
                baselines.extend(ParseTestcaseYaml(os.path.join(os.path.abspath(os.path.dirname(filepath)), include_yaml)))
        else:
            if data['baselines'] is None:
                return baselines
            for baseline in data['baselines']:
                bl = {
                    "host": baseline["host"] if "host" in baseline else "",
                    "path": baseline["path"] if "path" in baseline else "",
                    "casename": baseline["casename"]
                }
                if bl["path"] and bl["path"][0] != "/":
                    bl["path"] = "/" + bl["path"]
                baselines.append(bl)
    return baselines
