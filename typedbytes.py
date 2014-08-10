# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Typed bytes types:
BYTES = 0
BYTE = 1
BOOL = 2
INT = 3
LONG = 4
FLOAT = 5
DOUBLE = 6
STRING = 7
VECTOR = 8
LIST = 9
MAP = 10
SHORT = 11
USHORT = 12
ULONG = 13
GUID = 13

# Application-specific types:
PICKLE = 100
BYTESTRING = 101

# Low-level types:
MARKER = 255


def classes():

    from cPickle import dumps, loads, UnpicklingError, HIGHEST_PROTOCOL
    from struct import pack, unpack, error as StructError
    from array import array
    try:
        from struct import Struct
    except ImportError:
        class Struct(object):
            def __init__(self, fmt):
                self.fmt = fmt
            def unpack(self, *args):
                return unpack(self.fmt, *args)
            def pack(self, *args):
                return pack(self.fmt, *args)

    from types import BooleanType, IntType, LongType, FloatType
    from types import UnicodeType, StringType, TupleType, ListType, DictType
    from datetime import datetime, date
    from decimal import Decimal

    UNICODE_ENCODING = 'utf8'

    unpack_type = Struct('!B').unpack
    unpack_byte = Struct('!b').unpack
    unpack_int = Struct('!i').unpack
    unpack_long = Struct('!q').unpack
    unpack_float = Struct('!f').unpack
    unpack_double = Struct('!d').unpack
    unpack_short  = Struct('!h').unpack
    unpack_ushort  = Struct('!H').unpack
    unpack_ulong = Struct('!L').unpack
    unpack_guid = Struct('!16b').unpack

    _len = len


    class Bytes(str):

        def __repr__(self):
            return "Bytes(" + str.__repr__(self) + ")"


    class Input(object):

        def __init__(self, file, unicode_errors='strict'):
            self.file = file
            self.unicode_errors = unicode_errors
            self.eof = False
            self.handler_table = self._make_handler_table()

        def _read(self):
            try:
                t = unpack_type(self.file.read(1))[0]
                self.t = t
            except StructError:
                self.eof = True
                raise StopIteration
            return self.handler_table[t](self)

        def read(self):
            try:
                return self._read()
            except StopIteration:
                return None

        def _reads(self):
            r = self._read
            while 1:
                yield r()

        __iter__ = reads = _reads

        def close(self):
            self.file.close()

        def read_bytes(self):
            count = unpack_int(self.file.read(4))[0]
            value = self.file.read(count)
            if _len(value) != count:
                raise StructError("EOF before reading all of bytes type")
            return Bytes(value)

        def read_byte(self):
            return unpack_byte(self.file.read(1))[0]

        def read_bool(self):
            return bool(unpack_byte(self.file.read(1))[0])

        def read_int(self):
            return unpack_int(self.file.read(4))[0]

        def read_long(self):
            return unpack_long(self.file.read(8))[0]

        def read_float(self):
            return unpack_float(self.file.read(4))[0]

        def read_double(self):
            return unpack_double(self.file.read(8))[0]

        def read_short(self):
            return unpack_short(self.file.read(2))[0]

        def read_ushort(self):
            return unpack_ushort(self.file.read(2))[0]

        def read_ulong(self):
            return unpack_ulong(self.file.read(8))[0]

        def read_guid(self):
            return unpack_guid(self.file.read(16))[0]

        def read_string(self):
            count = unpack_int(self.file.read(4))[0]
            value = self.file.read(count)
            if _len(value) != count:
                raise StructError("EOF before reading all of string")
            return value

        read_bytestring = read_string

        def read_unicode(self):
            count = unpack_int(self.file.read(4))[0]
            value = self.file.read(count)
            if _len(value) != count:
                raise StructError("EOF before reading all of string")
            return value.decode(UNICODE_ENCODING, self.unicode_errors)

        def read_vector(self):
            r = self._read
            count = unpack_int(self.file.read(4))[0]
            try:
                return tuple(r() for i in xrange(count))
            except StopIteration:
                raise StructError("EOF before all vector elements read")

        def read_list(self):
            value = list(self._reads())
            if self.eof:
                raise StructError("EOF before end-of-list marker")
            return value

        def read_map(self):
            r = self._read
            count = unpack_int(self.file.read(4))[0]
            return dict((r(), r()) for i in xrange(count))

        def read_pickle(self):
            count = unpack_int(self.file.read(4))[0]
            bytes = self.file.read(count)
            if _len(bytes) != count:
                raise StructError("EOF before reading all of bytes type")
            return loads(bytes)

        def read_marker(self):
            raise StopIteration

        def invalid_typecode(self):
            raise StructError("Invalid type byte: " + str(self.t))

        TYPECODE_HANDLER_MAP = {
            BYTES: read_bytes,
            BYTE: read_byte,
            BOOL: read_bool,
            INT: read_int,
            LONG: read_long,
            FLOAT: read_float,
            DOUBLE: read_double,
            SHORT:read_short,
            USHORT:read_ushort,
            ULONG:read_ulong,
            GUID:read_guid,
            STRING: read_string,
            VECTOR: read_vector,
            LIST: read_list,
            MAP: read_map,
            PICKLE: read_pickle,
            BYTESTRING: read_bytestring,
            MARKER: read_marker
        }

        def _make_handler_table(self):
            return list(Input.TYPECODE_HANDLER_MAP.get(i,
                        Input.invalid_typecode) for i in xrange(256))

        def register(self, typecode, handler):
            self.handler_table[typecode] = handler

        def lookup(self, typecode):
            return lambda: self.handler_table[typecode](self)


    _BYTES, _BYTE, _BOOL = BYTES, BYTE, BOOL
    _INT, _LONG, _FLOAT, _DOUBLE = INT, LONG, FLOAT, DOUBLE
    _STRING, _VECTOR, _LIST, _MAP = STRING, VECTOR, LIST, MAP
    _PICKLE, _BYTESTRING, _MARKER = PICKLE, BYTESTRING, MARKER

    LIST_CODE, MARKER_CODE = (pack('!B', i) for i in (LIST, MARKER))

    pack_byte = Struct('!b').pack
    pack_int = Struct('!i').pack
    pack_long = Struct('!q').pack
    pack_float = Struct('!f').pack
    pack_double = Struct('!d').pack
    pack_short  = Struct('!h').pack
    pack_ushort  = Struct('!H').pack
    pack_ulong = Struct('!L').pack
    pack_guid = Struct('!16b').pack

    _int, _type = int, type


    def flatten(iterable):
        for i in iterable:
            for j in i:
                yield j


    class Output(object):

        def __init__(self, file, unicode_errors='strict'):
            self.file = file
            self.unicode_errors = unicode_errors
            self.handler_map = self._make_handler_map()

        def __del__(self):
            if not file.closed:
                self.file.flush()

        def _write(self, obj):
            try:
                writefunc = self.handler_map[_type(obj)]
            except KeyError:
                writefunc = Output.write_pickle
            writefunc(self, obj)

        write = _write

        def _writes(self, iterable):
            w = self._write
            for obj in iterable:
                w(obj)

        writes = _writes

        def flush(self):
            self.file.flush()

        def close(self):
            self.file.close()

        def write_bytes(self, bytes):
            self.file.write(pack_int(_len(bytes)))
            self.file.write(bytes)

        def write_byte(self, byte):
            self.file.write(pack_byte(byte))

        def write_bool(self, bool_):
            self.file.write(pack_byte(_int(bool_)))

        def write_int(self, int_):
            # Python ints are 64-bit
            if -2147483648 <= int_ <= 2147483647:
                self.file.write(pack_int(int_))
            else:
                self.file.write(pack_long(int_))

        def write_long(self, long_):
            # Python longs are infinite precision
            if -9223372036854775808L <= long_ <= 9223372036854775807L:
                self.file.write(pack_long(long_))
            else:
                self.write_pickle(long_)

        def write_float(self, float_):
            self.file.write(pack_float(float_))

        def write_double(self, double):
            self.file.write(pack_double(double))

        def write_short(self,short_):
            return self.file.write(pack_short(short_))

        def write_ushort(self, ushort_):
            return self.file.write(pack_ushort(ushort_))

        def write_ulong(self, ulong_):
            return self.file.write(pack_ulong(ulong_))

        def write_guid(self, guid_):
            return self.file.write(pack_guid(guid_))

        def write_string(self, string):
            self.file.write(pack_int(_len(string)))
            self.file.write(string)

        def write_bytestring(self, string):
            self.file.write(pack_int(_len(string)))
            self.file.write(string)

        def write_unicode(self, string):
            string = string.encode(UNICODE_ENCODING, self.unicode_errors)
            self.file.write(pack_int(_len(string)))
            self.file.write(string)

        def write_vector(self, vector):
            self.file.write(pack_int(_len(vector)))
            self._writes(vector)

        def write_list(self, list_):
            self.file.write(LIST_CODE)
            self._writes(list_)
            self.file.write(MARKER_CODE)

        def write_map(self, map):
            self.file.write(pack_int(_len(map)))
            self._writes(flatten(map.iteritems()))

        def write_pickle(self, obj):
            bytes = dumps(obj, HIGHEST_PROTOCOL)
            self.file.write(pack_int(_len(bytes)))
            self.file.write(bytes)

        def write_array(self, arr):
            bytes = arr.tostring()
            self.file.write(pack_int(_len(bytes)))
            self.file.write(bytes)

        TYPE_HANDLER_MAP = {
            BooleanType: write_bool,
            IntType: write_int,
            LongType: write_long,
            FloatType: write_double,
            StringType: write_string,
            SHORT:write_short,
            USHORT:write_ushort,
            ULONG:write_ulong,
            GUID:write_guid,
            TupleType: write_vector,
            ListType: write_list,
            DictType: write_map,
            UnicodeType: write_unicode,
            Bytes: write_bytes,
            datetime: write_pickle,
            date: write_pickle,
            Decimal: write_pickle,
            array: write_array
        }

        def _make_handler_map(self):
            return dict(Output.TYPE_HANDLER_MAP)

        def register(self, python_type, handler):
            self.handler_map[python_type] = handler

        def lookup(self, python_type):
            handler_map = self.handler_map
            if python_type in handler_map:
                return lambda obj: handler_map[python_type](self, obj)
            else:
                return lambda obj: Output.write_pickle(self, obj)


    class PairedInput(Input):

        def read(self):
            try:
                key = self._read()
            except StopIteration:
                return None
            try:
                value = self._read()
            except StopIteration:
                raise StructError('EOF before second item in pair')
            return key, value

        def reads(self):
            it = self._reads()
            next = it.next
            while 1:
                key = next()
                try:
                    value = next()
                except StopIteration:
                    raise StructError('EOF before second item in pair')
                yield key, value

        __iter__ = reads


    class PairedOutput(Output):

        def write(self, pair):
            self._writes(pair)

        def writes(self, iterable):
            self._writes(flatten(iterable))


    return Input, Output, PairedInput, PairedOutput, Bytes


Input, Output, PairedInput, PairedOutput, Bytes = classes()
