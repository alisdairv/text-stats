from sys import getsizeof

def read_chunks(filehandle, chunksize):
    nextline = filehandle.readline()
    str = ""
    while nextline != "":
        str = str + nextline
        if getsizeof(str) > chunksize:
            yield str
            str = ""
        nextline = filehandle.readline()
    yield str
