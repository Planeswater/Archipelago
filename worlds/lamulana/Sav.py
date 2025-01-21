# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import ReadWriteKaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Sav(ReadWriteKaitaiStruct):
    def __init__(self, _io=None, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self

    def _read(self):
        self.valid = self._io.read_u1()
        self.game_time = self._io.read_u4be()
        self.zone = self._io.read_u1()
        self.room = self._io.read_u1()
        self.screen = self._io.read_u1()
        self.x_position = self._io.read_u2be()
        self.y_position = self._io.read_u2be()
        self.max_hp = self._io.read_u1()
        self.current_hp = self._io.read_u2be()
        self.current_exp = self._io.read_u2be()
        self.flags = []
        for i in range(4096):
            self.flags.append(self._io.read_u1())

        self.inventory = []
        for i in range(255):
            self.inventory.append(self._io.read_u2be())

        self.held_main_weapon = self._io.read_u1()
        self.held_sub_weapon = self._io.read_u1()
        self.held_use_item = self._io.read_u1()
        self.held_main_weapon_slot = self._io.read_u1()
        self.held_sub_weapon_slot = self._io.read_u1()
        self.held_use_item_slot = self._io.read_u1()
        self.num_emails = self._io.read_u2be()
        self.received_emails = self._io.read_u2be()
        self.emails = []
        for i in range(self.num_emails):
            _t_emails = Sav.Email(self._io, self, self._root)
            _t_emails._read()
            self.emails.append(_t_emails)

        self.equipped_software = []
        for i in range(20):
            self.equipped_software.append(self._io.read_u1())

        self.rosettas_read = []
        for i in range(3):
            self.rosettas_read.append(self._io.read_u2be())

        self.bunemon_records = []
        for i in range(20):
            _t_bunemon_records = Sav.BunemonRecord(self._io, self, self._root)
            _t_bunemon_records._read()
            self.bunemon_records.append(_t_bunemon_records)

        self.mantras_learned = []
        for i in range(10):
            self.mantras_learned.append(self._io.read_u1())

        self.maps_owned_bit_array = self._io.read_u4be()


    def _fetch_instances(self):
        pass
        for i in range(len(self.flags)):
            pass

        for i in range(len(self.inventory)):
            pass

        for i in range(len(self.emails)):
            pass
            self.emails[i]._fetch_instances()

        for i in range(len(self.equipped_software)):
            pass

        for i in range(len(self.rosettas_read)):
            pass

        for i in range(len(self.bunemon_records)):
            pass
            self.bunemon_records[i]._fetch_instances()

        for i in range(len(self.mantras_learned)):
            pass



    def _write__seq(self, io=None):
        super(Sav, self)._write__seq(io)
        self._io.write_u1(self.valid)
        self._io.write_u4be(self.game_time)
        self._io.write_u1(self.zone)
        self._io.write_u1(self.room)
        self._io.write_u1(self.screen)
        self._io.write_u2be(self.x_position)
        self._io.write_u2be(self.y_position)
        self._io.write_u1(self.max_hp)
        self._io.write_u2be(self.current_hp)
        self._io.write_u2be(self.current_exp)
        for i in range(len(self.flags)):
            pass
            self._io.write_u1(self.flags[i])

        for i in range(len(self.inventory)):
            pass
            self._io.write_u2be(self.inventory[i])

        self._io.write_u1(self.held_main_weapon)
        self._io.write_u1(self.held_sub_weapon)
        self._io.write_u1(self.held_use_item)
        self._io.write_u1(self.held_main_weapon_slot)
        self._io.write_u1(self.held_sub_weapon_slot)
        self._io.write_u1(self.held_use_item_slot)
        self._io.write_u2be(self.num_emails)
        self._io.write_u2be(self.received_emails)
        for i in range(len(self.emails)):
            pass
            self.emails[i]._write__seq(self._io)

        for i in range(len(self.equipped_software)):
            pass
            self._io.write_u1(self.equipped_software[i])

        for i in range(len(self.rosettas_read)):
            pass
            self._io.write_u2be(self.rosettas_read[i])

        for i in range(len(self.bunemon_records)):
            pass
            self.bunemon_records[i]._write__seq(self._io)

        for i in range(len(self.mantras_learned)):
            pass
            self._io.write_u1(self.mantras_learned[i])

        self._io.write_u4be(self.maps_owned_bit_array)


    def _check(self):
        pass
        if (len(self.flags) != 4096):
            raise kaitaistruct.ConsistencyError(u"flags", len(self.flags), 4096)
        for i in range(len(self.flags)):
            pass

        if (len(self.inventory) != 255):
            raise kaitaistruct.ConsistencyError(u"inventory", len(self.inventory), 255)
        for i in range(len(self.inventory)):
            pass

        if (len(self.emails) != self.num_emails):
            raise kaitaistruct.ConsistencyError(u"emails", len(self.emails), self.num_emails)
        for i in range(len(self.emails)):
            pass
            if self.emails[i]._root != self._root:
                raise kaitaistruct.ConsistencyError(u"emails", self.emails[i]._root, self._root)
            if self.emails[i]._parent != self:
                raise kaitaistruct.ConsistencyError(u"emails", self.emails[i]._parent, self)

        if (len(self.equipped_software) != 20):
            raise kaitaistruct.ConsistencyError(u"equipped_software", len(self.equipped_software), 20)
        for i in range(len(self.equipped_software)):
            pass

        if (len(self.rosettas_read) != 3):
            raise kaitaistruct.ConsistencyError(u"rosettas_read", len(self.rosettas_read), 3)
        for i in range(len(self.rosettas_read)):
            pass

        if (len(self.bunemon_records) != 20):
            raise kaitaistruct.ConsistencyError(u"bunemon_records", len(self.bunemon_records), 20)
        for i in range(len(self.bunemon_records)):
            pass
            if self.bunemon_records[i]._root != self._root:
                raise kaitaistruct.ConsistencyError(u"bunemon_records", self.bunemon_records[i]._root, self._root)
            if self.bunemon_records[i]._parent != self:
                raise kaitaistruct.ConsistencyError(u"bunemon_records", self.bunemon_records[i]._parent, self)

        if (len(self.mantras_learned) != 10):
            raise kaitaistruct.ConsistencyError(u"mantras_learned", len(self.mantras_learned), 10)
        for i in range(len(self.mantras_learned)):
            pass


    class Email(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.screenplay_card = self._io.read_u2be()
            self.game_time_received = self._io.read_u4be()
            self.mail_number = self._io.read_u2be()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Sav.Email, self)._write__seq(io)
            self._io.write_u2be(self.screenplay_card)
            self._io.write_u4be(self.game_time_received)
            self._io.write_u2be(self.mail_number)


        def _check(self):
            pass


    class BunemonRecord(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.slot_number = self._io.read_u1()
            self.field_map_card = self._io.read_u2be()
            self.field_map_record = self._io.read_u2be()
            self.location_card = self._io.read_u2be()
            self.location_record = self._io.read_u2be()
            self.text_card = self._io.read_u2be()
            self.text_record = self._io.read_u2be()
            self.is_tablet = self._io.read_u1()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Sav.BunemonRecord, self)._write__seq(io)
            self._io.write_u1(self.slot_number)
            self._io.write_u2be(self.field_map_card)
            self._io.write_u2be(self.field_map_record)
            self._io.write_u2be(self.location_card)
            self._io.write_u2be(self.location_record)
            self._io.write_u2be(self.text_card)
            self._io.write_u2be(self.text_record)
            self._io.write_u1(self.is_tablet)


        def _check(self):
            pass
