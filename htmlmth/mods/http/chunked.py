import random

def _chunk_data(data, min_chunk_size=None, max_chunk_size=None, leadingzeros=0):
    dl = len(data)
    if max_chunk_size is None:
        max_chunk_size = dl
    chunk_sizes = []
    while dl > 0:
        max_chunk_size = min(dl, max_chunk_size)
        if dl <= min_chunk_size:
            min_chunk_size = dl
        chunk_size = random.randint(min_chunk_size, max_chunk_size)
        chunk_sizes.append(chunk_size)
        dl -= chunk_size
    ret = ""

    chunk_sized = 0
    for chunk_size in chunk_sizes:
        ret += "0"*leadingzeros + "%s\r\n" % (hex(chunk_size)[2:])
        ret += "%s\r\n" % (data[chunk_sized:chunk_sized + chunk_size])
        chunk_sized += chunk_size
    ret += "0\r\n\r\n"
    return ret

def encode_chunked_equisize(content, chunksize=256, leadingzeros=0):
    return _chunk_data(content, min_chunk_size=chunksize, max_chunk_size=chunksize, leadingzeros=leadingzeros)


def encode_chunked_varysize(content, min_chunksize=128, max_chunksize=256, leadingzeros=0):
    return _chunk_data(content, min_chunk_size=min_chunksize, max_chunk_size=max_chunksize, leadingzeros=leadingzeros)

