import StringIO
import gzip

def encode_gzip(content, compresslevel=9):
    out = StringIO.StringIO()
    f = gzip.GzipFile(fileobj=out, mode='w', compresslevel=compresslevel)
    f.write(content)
    f.close()
    return out.getvalue()
