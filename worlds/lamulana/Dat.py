# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import ReadWriteKaitaiStruct, KaitaiStream, BytesIO
from enum import IntEnum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Dat(ReadWriteKaitaiStruct):

    class EntryHeader(IntEnum):
        flag = 64
        flag2 = 65
        item = 66
        pose = 70
        mantra = 71
        color = 74
        item_name = 77
        data = 78
        anime = 79
    def __init__(self, _io=None, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self

    def _read(self):
        self.num_cards = self._io.read_u2be()
        self.cards = []
        for i in range(self.num_cards):
            _t_cards = Dat.Card(self._io, self, self._root)
            _t_cards._read()
            self.cards.append(_t_cards)



    def _fetch_instances(self):
        pass
        for i in range(len(self.cards)):
            pass
            self.cards[i]._fetch_instances()



    def _write__seq(self, io=None):
        super(Dat, self)._write__seq(io)
        self._io.write_u2be(self.num_cards)
        for i in range(len(self.cards)):
            pass
            self.cards[i]._write__seq(self._io)



    def _check(self):
        pass
        if (len(self.cards) != self.num_cards):
            raise kaitaistruct.ConsistencyError(u"cards", len(self.cards), self.num_cards)
        for i in range(len(self.cards)):
            pass
            if self.cards[i]._root != self._root:
                raise kaitaistruct.ConsistencyError(u"cards", self.cards[i]._root, self._root)
            if self.cards[i]._parent != self:
                raise kaitaistruct.ConsistencyError(u"cards", self.cards[i]._parent, self)


    class Entry(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.header = KaitaiStream.resolve_enum(Dat.EntryHeader, self._io.read_u2be())
            _on = self.header
            if _on == Dat.EntryHeader.anime:
                pass
                self.contents = Dat.Anime(self._io, self, self._root)
                self.contents._read()
            elif _on == Dat.EntryHeader.flag2:
                pass
                self.contents = Dat.Flag2(self._io, self, self._root)
                self.contents._read()
            elif _on == Dat.EntryHeader.color:
                pass
                self.contents = Dat.Color(self._io, self, self._root)
                self.contents._read()
            elif _on == Dat.EntryHeader.flag:
                pass
                self.contents = Dat.Flag(self._io, self, self._root)
                self.contents._read()
            elif _on == Dat.EntryHeader.item_name:
                pass
                self.contents = Dat.ItemName(self._io, self, self._root)
                self.contents._read()
            elif _on == Dat.EntryHeader.pose:
                pass
                self.contents = Dat.Pose(self._io, self, self._root)
                self.contents._read()
            elif _on == Dat.EntryHeader.data:
                pass
                self.contents = Dat.Data(self._io, self, self._root)
                self.contents._read()
            elif _on == Dat.EntryHeader.item:
                pass
                self.contents = Dat.Item(self._io, self, self._root)
                self.contents._read()
            elif _on == Dat.EntryHeader.mantra:
                pass
                self.contents = Dat.Mantra(self._io, self, self._root)
                self.contents._read()
            else:
                pass
                self.contents = Dat.Noop(self._io, self, self._root)
                self.contents._read()


        def _fetch_instances(self):
            pass
            _on = self.header
            if _on == Dat.EntryHeader.anime:
                pass
                self.contents._fetch_instances()
            elif _on == Dat.EntryHeader.flag2:
                pass
                self.contents._fetch_instances()
            elif _on == Dat.EntryHeader.color:
                pass
                self.contents._fetch_instances()
            elif _on == Dat.EntryHeader.flag:
                pass
                self.contents._fetch_instances()
            elif _on == Dat.EntryHeader.item_name:
                pass
                self.contents._fetch_instances()
            elif _on == Dat.EntryHeader.pose:
                pass
                self.contents._fetch_instances()
            elif _on == Dat.EntryHeader.data:
                pass
                self.contents._fetch_instances()
            elif _on == Dat.EntryHeader.item:
                pass
                self.contents._fetch_instances()
            elif _on == Dat.EntryHeader.mantra:
                pass
                self.contents._fetch_instances()
            else:
                pass
                self.contents._fetch_instances()


        def _write__seq(self, io=None):
            super(Dat.Entry, self)._write__seq(io)
            self._io.write_u2be(int(self.header))
            _on = self.header
            if _on == Dat.EntryHeader.anime:
                pass
                self.contents._write__seq(self._io)
            elif _on == Dat.EntryHeader.flag2:
                pass
                self.contents._write__seq(self._io)
            elif _on == Dat.EntryHeader.color:
                pass
                self.contents._write__seq(self._io)
            elif _on == Dat.EntryHeader.flag:
                pass
                self.contents._write__seq(self._io)
            elif _on == Dat.EntryHeader.item_name:
                pass
                self.contents._write__seq(self._io)
            elif _on == Dat.EntryHeader.pose:
                pass
                self.contents._write__seq(self._io)
            elif _on == Dat.EntryHeader.data:
                pass
                self.contents._write__seq(self._io)
            elif _on == Dat.EntryHeader.item:
                pass
                self.contents._write__seq(self._io)
            elif _on == Dat.EntryHeader.mantra:
                pass
                self.contents._write__seq(self._io)
            else:
                pass
                self.contents._write__seq(self._io)


        def _check(self):
            pass
            _on = self.header
            if _on == Dat.EntryHeader.anime:
                pass
                if self.contents._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._root, self._root)
                if self.contents._parent != self:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._parent, self)
            elif _on == Dat.EntryHeader.flag2:
                pass
                if self.contents._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._root, self._root)
                if self.contents._parent != self:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._parent, self)
            elif _on == Dat.EntryHeader.color:
                pass
                if self.contents._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._root, self._root)
                if self.contents._parent != self:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._parent, self)
            elif _on == Dat.EntryHeader.flag:
                pass
                if self.contents._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._root, self._root)
                if self.contents._parent != self:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._parent, self)
            elif _on == Dat.EntryHeader.item_name:
                pass
                if self.contents._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._root, self._root)
                if self.contents._parent != self:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._parent, self)
            elif _on == Dat.EntryHeader.pose:
                pass
                if self.contents._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._root, self._root)
                if self.contents._parent != self:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._parent, self)
            elif _on == Dat.EntryHeader.data:
                pass
                if self.contents._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._root, self._root)
                if self.contents._parent != self:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._parent, self)
            elif _on == Dat.EntryHeader.item:
                pass
                if self.contents._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._root, self._root)
                if self.contents._parent != self:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._parent, self)
            elif _on == Dat.EntryHeader.mantra:
                pass
                if self.contents._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._root, self._root)
                if self.contents._parent != self:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._parent, self)
            else:
                pass
                if self.contents._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._root, self._root)
                if self.contents._parent != self:
                    raise kaitaistruct.ConsistencyError(u"contents", self.contents._parent, self)


    class Data(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.num_values = self._io.read_s2be()
            self.values = []
            for i in range(self.num_values):
                self.values.append(self._io.read_s2be())



        def _fetch_instances(self):
            pass
            for i in range(len(self.values)):
                pass



        def _write__seq(self, io=None):
            super(Dat.Data, self)._write__seq(io)
            self._io.write_s2be(self.num_values)
            for i in range(len(self.values)):
                pass
                self._io.write_s2be(self.values[i])



        def _check(self):
            pass
            if (len(self.values) != self.num_values):
                raise kaitaistruct.ConsistencyError(u"values", len(self.values), self.num_values)
            for i in range(len(self.values)):
                pass



    class Mantra(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.value = self._io.read_s2be()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Dat.Mantra, self)._write__seq(io)
            self._io.write_s2be(self.value)


        def _check(self):
            pass


    class Color(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.red = self._io.read_s2be()
            self.green = self._io.read_s2be()
            self.blue = self._io.read_s2be()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Dat.Color, self)._write__seq(io)
            self._io.write_s2be(self.red)
            self._io.write_s2be(self.green)
            self._io.write_s2be(self.blue)


        def _check(self):
            pass


    class Noop(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.no_value = self._io.read_bytes(0)


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Dat.Noop, self)._write__seq(io)
            self._io.write_bytes(self.no_value)


        def _check(self):
            pass
            if (len(self.no_value) != 0):
                raise kaitaistruct.ConsistencyError(u"no_value", len(self.no_value), 0)


    class ItemName(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.value = self._io.read_s2be()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Dat.ItemName, self)._write__seq(io)
            self._io.write_s2be(self.value)


        def _check(self):
            pass


    class CardContents(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.entries = []
            i = 0
            while not self._io.is_eof():
                _t_entries = Dat.Entry(self._io, self, self._root)
                _t_entries._read()
                self.entries.append(_t_entries)
                i += 1



        def _fetch_instances(self):
            pass
            for i in range(len(self.entries)):
                pass
                self.entries[i]._fetch_instances()



        def _write__seq(self, io=None):
            super(Dat.CardContents, self)._write__seq(io)
            for i in range(len(self.entries)):
                pass
                if self._io.is_eof():
                    raise kaitaistruct.ConsistencyError(u"entries", self._io.size() - self._io.pos(), 0)
                self.entries[i]._write__seq(self._io)

            if not self._io.is_eof():
                raise kaitaistruct.ConsistencyError(u"entries", self._io.size() - self._io.pos(), 0)


        def _check(self):
            pass
            for i in range(len(self.entries)):
                pass
                if self.entries[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"entries", self.entries[i]._root, self._root)
                if self.entries[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"entries", self.entries[i]._parent, self)



    class Flag(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.address = self._io.read_s2be()
            self.value = self._io.read_s2be()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Dat.Flag, self)._write__seq(io)
            self._io.write_s2be(self.address)
            self._io.write_s2be(self.value)


        def _check(self):
            pass


    class Pose(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.value = self._io.read_s2be()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Dat.Pose, self)._write__seq(io)
            self._io.write_s2be(self.value)


        def _check(self):
            pass


    class Anime(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.value = self._io.read_s2be()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Dat.Anime, self)._write__seq(io)
            self._io.write_s2be(self.value)


        def _check(self):
            pass


    class Card(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.len_contents = self._io.read_u2be()
            self._raw_contents = self._io.read_bytes(self.len_contents)
            _io__raw_contents = KaitaiStream(BytesIO(self._raw_contents))
            self.contents = Dat.CardContents(_io__raw_contents, self, self._root)
            self.contents._read()


        def _fetch_instances(self):
            pass
            self.contents._fetch_instances()


        def _write__seq(self, io=None):
            super(Dat.Card, self)._write__seq(io)
            self._io.write_u2be(self.len_contents)
            _io__raw_contents = KaitaiStream(BytesIO(bytearray(self.len_contents)))
            self._io.add_child_stream(_io__raw_contents)
            _pos2 = self._io.pos()
            self._io.seek(self._io.pos() + (self.len_contents))
            def handler(parent, _io__raw_contents=_io__raw_contents):
                self._raw_contents = _io__raw_contents.to_byte_array()
                if (len(self._raw_contents) != self.len_contents):
                    raise kaitaistruct.ConsistencyError(u"raw(contents)", len(self._raw_contents), self.len_contents)
                parent.write_bytes(self._raw_contents)
            _io__raw_contents.write_back_handler = KaitaiStream.WriteBackHandler(_pos2, handler)
            self.contents._write__seq(_io__raw_contents)


        def _check(self):
            pass
            if self.contents._root != self._root:
                raise kaitaistruct.ConsistencyError(u"contents", self.contents._root, self._root)
            if self.contents._parent != self:
                raise kaitaistruct.ConsistencyError(u"contents", self.contents._parent, self)


    class Flag2(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.address = self._io.read_s2be()
            self.value = self._io.read_s2be()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Dat.Flag2, self)._write__seq(io)
            self._io.write_s2be(self.address)
            self._io.write_s2be(self.value)


        def _check(self):
            pass


    class Item(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.value = self._io.read_s2be()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Dat.Item, self)._write__seq(io)
            self._io.write_s2be(self.value)


        def _check(self):
            pass
