# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import ReadWriteKaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Rcd(ReadWriteKaitaiStruct):
    def __init__(self, _io=None, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self

    def _read(self):
        self.unknown = self._io.read_s2be()
        self.zones = []
        for i in range(26):
            _t_zones = Rcd.Zone(i, self._io, self, self._root)
            _t_zones._read()
            self.zones.append(_t_zones)

        self.padding = (self._io.read_bytes_full()).decode("UTF-8")


    def _fetch_instances(self):
        pass
        for i in range(len(self.zones)):
            pass
            self.zones[i]._fetch_instances()



    def _write__seq(self, io=None):
        super(Rcd, self)._write__seq(io)
        self._io.write_s2be(self.unknown)
        for i in range(len(self.zones)):
            pass
            self.zones[i]._write__seq(self._io)

        self._io.write_bytes((self.padding).encode(u"UTF-8"))
        if not self._io.is_eof():
            raise kaitaistruct.ConsistencyError(u"padding", self._io.size() - self._io.pos(), 0)


    def _check(self):
        pass
        if (len(self.zones) != 26):
            raise kaitaistruct.ConsistencyError(u"zones", len(self.zones), 26)
        for i in range(len(self.zones)):
            pass
            if self.zones[i]._root != self._root:
                raise kaitaistruct.ConsistencyError(u"zones", self.zones[i]._root, self._root)
            if self.zones[i]._parent != self:
                raise kaitaistruct.ConsistencyError(u"zones", self.zones[i]._parent, self)
            if (self.zones[i].zone_index != i):
                raise kaitaistruct.ConsistencyError(u"zones", self.zones[i].zone_index, i)


    class ObjectWithoutPosition(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.id = self._io.read_s2be()
            self.test_operations_length = self._io.read_bits_int_be(4)
            self.write_operations_length = self._io.read_bits_int_be(4)
            self.parameters_length = self._io.read_s1()
            self.test_operations = []
            for i in range(self.test_operations_length):
                _t_test_operations = Rcd.Operation(self._io, self, self._root)
                _t_test_operations._read()
                self.test_operations.append(_t_test_operations)

            self.write_operations = []
            for i in range(self.write_operations_length):
                _t_write_operations = Rcd.Operation(self._io, self, self._root)
                _t_write_operations._read()
                self.write_operations.append(_t_write_operations)

            self.parameters = []
            for i in range(self.parameters_length):
                self.parameters.append(self._io.read_s2be())



        def _fetch_instances(self):
            pass
            for i in range(len(self.test_operations)):
                pass
                self.test_operations[i]._fetch_instances()

            for i in range(len(self.write_operations)):
                pass
                self.write_operations[i]._fetch_instances()

            for i in range(len(self.parameters)):
                pass



        def _write__seq(self, io=None):
            super(Rcd.ObjectWithoutPosition, self)._write__seq(io)
            self._io.write_s2be(self.id)
            self._io.write_bits_int_be(4, self.test_operations_length)
            self._io.write_bits_int_be(4, self.write_operations_length)
            self._io.write_s1(self.parameters_length)
            for i in range(len(self.test_operations)):
                pass
                self.test_operations[i]._write__seq(self._io)

            for i in range(len(self.write_operations)):
                pass
                self.write_operations[i]._write__seq(self._io)

            for i in range(len(self.parameters)):
                pass
                self._io.write_s2be(self.parameters[i])



        def _check(self):
            pass
            if (len(self.test_operations) != self.test_operations_length):
                raise kaitaistruct.ConsistencyError(u"test_operations", len(self.test_operations), self.test_operations_length)
            for i in range(len(self.test_operations)):
                pass
                if self.test_operations[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"test_operations", self.test_operations[i]._root, self._root)
                if self.test_operations[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"test_operations", self.test_operations[i]._parent, self)

            if (len(self.write_operations) != self.write_operations_length):
                raise kaitaistruct.ConsistencyError(u"write_operations", len(self.write_operations), self.write_operations_length)
            for i in range(len(self.write_operations)):
                pass
                if self.write_operations[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"write_operations", self.write_operations[i]._root, self._root)
                if self.write_operations[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"write_operations", self.write_operations[i]._parent, self)

            if (len(self.parameters) != self.parameters_length):
                raise kaitaistruct.ConsistencyError(u"parameters", len(self.parameters), self.parameters_length)
            for i in range(len(self.parameters)):
                pass



    class Operation(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.flag = self._io.read_s2be()
            self.op_value = self._io.read_s1()
            self.operation = self._io.read_s1()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Rcd.Operation, self)._write__seq(io)
            self._io.write_s2be(self.flag)
            self._io.write_s1(self.op_value)
            self._io.write_s1(self.operation)


        def _check(self):
            pass


    class Screen(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.screen_name_length = self._io.read_s1()
            self.objects_length = self._io.read_s2be()
            self.objects_without_position_length = self._io.read_s1()
            self.objects_without_position = []
            for i in range(self.objects_without_position_length):
                _t_objects_without_position = Rcd.ObjectWithoutPosition(self._io, self, self._root)
                _t_objects_without_position._read()
                self.objects_without_position.append(_t_objects_without_position)

            self.objects_with_position = []
            for i in range((self.objects_length - self.objects_without_position_length)):
                _t_objects_with_position = Rcd.ObjectWithPosition(self._io, self, self._root)
                _t_objects_with_position._read()
                self.objects_with_position.append(_t_objects_with_position)

            self.screen_name = []
            for i in range(self.screen_name_length):
                self.screen_name.append(self._io.read_s1())

            self.exits = []
            for i in range(4):
                _t_exits = Rcd.Exit(self._io, self, self._root)
                _t_exits._read()
                self.exits.append(_t_exits)



        def _fetch_instances(self):
            pass
            for i in range(len(self.objects_without_position)):
                pass
                self.objects_without_position[i]._fetch_instances()

            for i in range(len(self.objects_with_position)):
                pass
                self.objects_with_position[i]._fetch_instances()

            for i in range(len(self.screen_name)):
                pass

            for i in range(len(self.exits)):
                pass
                self.exits[i]._fetch_instances()



        def _write__seq(self, io=None):
            super(Rcd.Screen, self)._write__seq(io)
            self._io.write_s1(self.screen_name_length)
            self._io.write_s2be(self.objects_length)
            self._io.write_s1(self.objects_without_position_length)
            for i in range(len(self.objects_without_position)):
                pass
                self.objects_without_position[i]._write__seq(self._io)

            for i in range(len(self.objects_with_position)):
                pass
                self.objects_with_position[i]._write__seq(self._io)

            for i in range(len(self.screen_name)):
                pass
                self._io.write_s1(self.screen_name[i])

            for i in range(len(self.exits)):
                pass
                self.exits[i]._write__seq(self._io)



        def _check(self):
            pass
            if (len(self.objects_without_position) != self.objects_without_position_length):
                raise kaitaistruct.ConsistencyError(u"objects_without_position", len(self.objects_without_position), self.objects_without_position_length)
            for i in range(len(self.objects_without_position)):
                pass
                if self.objects_without_position[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"objects_without_position", self.objects_without_position[i]._root, self._root)
                if self.objects_without_position[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"objects_without_position", self.objects_without_position[i]._parent, self)

            if (len(self.objects_with_position) != (self.objects_length - self.objects_without_position_length)):
                raise kaitaistruct.ConsistencyError(u"objects_with_position", len(self.objects_with_position), (self.objects_length - self.objects_without_position_length))
            for i in range(len(self.objects_with_position)):
                pass
                if self.objects_with_position[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"objects_with_position", self.objects_with_position[i]._root, self._root)
                if self.objects_with_position[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"objects_with_position", self.objects_with_position[i]._parent, self)

            if (len(self.screen_name) != self.screen_name_length):
                raise kaitaistruct.ConsistencyError(u"screen_name", len(self.screen_name), self.screen_name_length)
            for i in range(len(self.screen_name)):
                pass

            if (len(self.exits) != 4):
                raise kaitaistruct.ConsistencyError(u"exits", len(self.exits), 4)
            for i in range(len(self.exits)):
                pass
                if self.exits[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"exits", self.exits[i]._root, self._root)
                if self.exits[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"exits", self.exits[i]._parent, self)



    class Exit(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.field_id = self._io.read_s1()
            self.room_id = self._io.read_s1()
            self.screen_id = self._io.read_s1()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Rcd.Exit, self)._write__seq(io)
            self._io.write_s1(self.field_id)
            self._io.write_s1(self.room_id)
            self._io.write_s1(self.screen_id)


        def _check(self):
            pass


    class Room(ReadWriteKaitaiStruct):
        def __init__(self, zone_index, room_index, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root
            self.zone_index = zone_index
            self.room_index = room_index

        def _read(self):
            self.objects_length = self._io.read_s2be()
            self.objects = []
            for i in range(self.objects_length):
                _t_objects = Rcd.ObjectWithoutPosition(self._io, self, self._root)
                _t_objects._read()
                self.objects.append(_t_objects)

            self.screens = []
            for i in range(KaitaiStream.byte_array_index(self._root.zone_sizes[self.zone_index], self.room_index)):
                _t_screens = Rcd.Screen(self._io, self, self._root)
                _t_screens._read()
                self.screens.append(_t_screens)



        def _fetch_instances(self):
            pass
            for i in range(len(self.objects)):
                pass
                self.objects[i]._fetch_instances()

            for i in range(len(self.screens)):
                pass
                self.screens[i]._fetch_instances()



        def _write__seq(self, io=None):
            super(Rcd.Room, self)._write__seq(io)
            self._io.write_s2be(self.objects_length)
            for i in range(len(self.objects)):
                pass
                self.objects[i]._write__seq(self._io)

            for i in range(len(self.screens)):
                pass
                self.screens[i]._write__seq(self._io)



        def _check(self):
            pass
            if (len(self.objects) != self.objects_length):
                raise kaitaistruct.ConsistencyError(u"objects", len(self.objects), self.objects_length)
            for i in range(len(self.objects)):
                pass
                if self.objects[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"objects", self.objects[i]._root, self._root)
                if self.objects[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"objects", self.objects[i]._parent, self)

            if (len(self.screens) != KaitaiStream.byte_array_index(self._root.zone_sizes[self.zone_index], self.room_index)):
                raise kaitaistruct.ConsistencyError(u"screens", len(self.screens), KaitaiStream.byte_array_index(self._root.zone_sizes[self.zone_index], self.room_index))
            for i in range(len(self.screens)):
                pass
                if self.screens[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"screens", self.screens[i]._root, self._root)
                if self.screens[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"screens", self.screens[i]._parent, self)



    class ObjectWithPosition(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.id = self._io.read_s2be()
            self.test_operations_length = self._io.read_bits_int_be(4)
            self.write_operations_length = self._io.read_bits_int_be(4)
            self.parameters_length = self._io.read_s1()
            self.x_pos = self._io.read_s2be()
            self.y_pos = self._io.read_s2be()
            self.test_operations = []
            for i in range(self.test_operations_length):
                _t_test_operations = Rcd.Operation(self._io, self, self._root)
                _t_test_operations._read()
                self.test_operations.append(_t_test_operations)

            self.write_operations = []
            for i in range(self.write_operations_length):
                _t_write_operations = Rcd.Operation(self._io, self, self._root)
                _t_write_operations._read()
                self.write_operations.append(_t_write_operations)

            self.parameters = []
            for i in range(self.parameters_length):
                self.parameters.append(self._io.read_s2be())



        def _fetch_instances(self):
            pass
            for i in range(len(self.test_operations)):
                pass
                self.test_operations[i]._fetch_instances()

            for i in range(len(self.write_operations)):
                pass
                self.write_operations[i]._fetch_instances()

            for i in range(len(self.parameters)):
                pass



        def _write__seq(self, io=None):
            super(Rcd.ObjectWithPosition, self)._write__seq(io)
            self._io.write_s2be(self.id)
            self._io.write_bits_int_be(4, self.test_operations_length)
            self._io.write_bits_int_be(4, self.write_operations_length)
            self._io.write_s1(self.parameters_length)
            self._io.write_s2be(self.x_pos)
            self._io.write_s2be(self.y_pos)
            for i in range(len(self.test_operations)):
                pass
                self.test_operations[i]._write__seq(self._io)

            for i in range(len(self.write_operations)):
                pass
                self.write_operations[i]._write__seq(self._io)

            for i in range(len(self.parameters)):
                pass
                self._io.write_s2be(self.parameters[i])



        def _check(self):
            pass
            if (len(self.test_operations) != self.test_operations_length):
                raise kaitaistruct.ConsistencyError(u"test_operations", len(self.test_operations), self.test_operations_length)
            for i in range(len(self.test_operations)):
                pass
                if self.test_operations[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"test_operations", self.test_operations[i]._root, self._root)
                if self.test_operations[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"test_operations", self.test_operations[i]._parent, self)

            if (len(self.write_operations) != self.write_operations_length):
                raise kaitaistruct.ConsistencyError(u"write_operations", len(self.write_operations), self.write_operations_length)
            for i in range(len(self.write_operations)):
                pass
                if self.write_operations[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"write_operations", self.write_operations[i]._root, self._root)
                if self.write_operations[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"write_operations", self.write_operations[i]._parent, self)

            if (len(self.parameters) != self.parameters_length):
                raise kaitaistruct.ConsistencyError(u"parameters", len(self.parameters), self.parameters_length)
            for i in range(len(self.parameters)):
                pass



    class Zone(ReadWriteKaitaiStruct):
        def __init__(self, zone_index, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root
            self.zone_index = zone_index

        def _read(self):
            self.zone_name_length = self._io.read_s1()
            self.objects_length = self._io.read_s2be()
            self.zone_name = []
            for i in range(self.zone_name_length):
                self.zone_name.append(self._io.read_s1())

            self.objects = []
            for i in range(self.objects_length):
                _t_objects = Rcd.ObjectWithoutPosition(self._io, self, self._root)
                _t_objects._read()
                self.objects.append(_t_objects)

            self.rooms = []
            for i in range(len(self._root.zone_sizes[self.zone_index])):
                _t_rooms = Rcd.Room(self.zone_index, i, self._io, self, self._root)
                _t_rooms._read()
                self.rooms.append(_t_rooms)



        def _fetch_instances(self):
            pass
            for i in range(len(self.zone_name)):
                pass

            for i in range(len(self.objects)):
                pass
                self.objects[i]._fetch_instances()

            for i in range(len(self.rooms)):
                pass
                self.rooms[i]._fetch_instances()



        def _write__seq(self, io=None):
            super(Rcd.Zone, self)._write__seq(io)
            self._io.write_s1(self.zone_name_length)
            self._io.write_s2be(self.objects_length)
            for i in range(len(self.zone_name)):
                pass
                self._io.write_s1(self.zone_name[i])

            for i in range(len(self.objects)):
                pass
                self.objects[i]._write__seq(self._io)

            for i in range(len(self.rooms)):
                pass
                self.rooms[i]._write__seq(self._io)



        def _check(self):
            pass
            if (len(self.zone_name) != self.zone_name_length):
                raise kaitaistruct.ConsistencyError(u"zone_name", len(self.zone_name), self.zone_name_length)
            for i in range(len(self.zone_name)):
                pass

            if (len(self.objects) != self.objects_length):
                raise kaitaistruct.ConsistencyError(u"objects", len(self.objects), self.objects_length)
            for i in range(len(self.objects)):
                pass
                if self.objects[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"objects", self.objects[i]._root, self._root)
                if self.objects[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"objects", self.objects[i]._parent, self)

            if (len(self.rooms) != len(self._root.zone_sizes[self.zone_index])):
                raise kaitaistruct.ConsistencyError(u"rooms", len(self.rooms), len(self._root.zone_sizes[self.zone_index]))
            for i in range(len(self.rooms)):
                pass
                if self.rooms[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rooms", self.rooms[i]._root, self._root)
                if self.rooms[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rooms", self.rooms[i]._parent, self)
                if (self.rooms[i].zone_index != self.zone_index):
                    raise kaitaistruct.ConsistencyError(u"rooms", self.rooms[i].zone_index, self.zone_index)
                if (self.rooms[i].room_index != i):
                    raise kaitaistruct.ConsistencyError(u"rooms", self.rooms[i].room_index, i)



    @property
    def zone_sizes(self):
        if hasattr(self, '_m_zone_sizes'):
            return self._m_zone_sizes

        self._m_zone_sizes = [b"\x02\x02\x02\x02\x03\x01\x02\x02\x02\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", b"\x03\x02\x02\x01\x03\x03\x02\x02\x02\x02\x04\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", b"\x02\x02\x02\x01\x01\x03\x02\x03\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", b"\x02\x03\x02\x01\x06\x01\x02\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", b"\x03\x01\x02\x05\x01\x02\x02\x02\x02\x00\x01\x01\x01\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00", b"\x02\x02\x03\x03\x01\x02\x01\x02\x02\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", b"\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", b"\x02\x02\x03\x03\x02\x02\x02\x02\x02\x02\x02\x03\x03\x02\x02\x03\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", b"\x02\x02\x04\x04\x04\x04\x00\x00\x00\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", b"\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", b"\x02\x02\x03\x01\x02\x02\x01\x03\x02\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", b"\x03\x02\x02\x01\x04\x02\x01\x02\x01\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", b"\x02\x02\x02\x01\x04\x02\x02\x01\x01\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", b"\x02\x02\x03\x02\x02\x02\x04\x03\x01\x00\x00\x00\x00\x00\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00", b"\x03\x02\x02\x02\x02\x02\x02\x02\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", b"\x02\x02\x02\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", b"\x02\x02\x02\x02\x03\x00\x00\x00\x00\x00\x00\x00\x00", b"\x02\x02\x02\x01\x02\x02\x01\x02\x02\x02\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", b"\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x00\x00\x00\x00\x00", b"\x02\x03\x02\x02\x02", b"\x02\x03\x02\x02\x02", b"\x02\x00", b"\x03\x02\x02\x01\x03\x03\x02\x02\x02\x02\x04\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", b"\x01\x02\x02\x01\x02\x02\x02\x01\x02\x02\x02\x01\x02\x01\x02\x02\x01\x01\x02\x01\x01\x01\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", b"\x02\x01\x02\x00\x00", b"\x05\x05\x05\x05\x00"]
        return getattr(self, '_m_zone_sizes', None)

    def _invalidate_zone_sizes(self):
        del self._m_zone_sizes
