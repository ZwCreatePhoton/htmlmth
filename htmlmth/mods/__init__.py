from htmlmth.utils import TransformFunctionArgument, MIME_TYPE_MAP, HttpMetaData


class Mod():
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
