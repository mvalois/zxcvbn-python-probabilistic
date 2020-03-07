import os
dirp = dir_path = os.path.dirname(os.path.realpath(__file__))
from cffi import FFI
ffibuilder = FFI()
ffibuilder.cdef(open(os.path.join(dirp, 'parse.h')).read())
ffibuilder.set_source("_parse", open(os.path.join(dirp, 'parse.c')).read(), libraries=[])
ffibuilder.compile(verbose=False)