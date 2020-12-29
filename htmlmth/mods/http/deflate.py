import zlib

def encode_deflate(content, compresslevel=9):
    return zlib.compress(content, compresslevel)[2:-4]
