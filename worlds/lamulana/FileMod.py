import io
import os
import Utils
from .Items import item_table
from .LmFlags import RCD_OBJECTS
from kaitaistruct import KaitaiStream


class FileMod:

    def __init__(self, mod_class, filename, local_config, options, filler_flags):
        file_path = Utils.user_path(filename)
        self.file_size = os.path.getsize(file_path)

        file_io = KaitaiStream(open(file_path, 'rb'))

        self.file_contents = mod_class(file_io)
        self.file_contents._read()

        self.local_config = local_config
        self.options = options
        self.filler_flags = filler_flags

    def write_file(self):
        write_io = KaitaiStream(io.BytesIO(bytearray(self.file_size)))
        self.file_contents._write(write_io)

        return write_io.to_byte_array()

    def set_params(self, params):
        location = params["location"]
        item_id = params["item_id"]
        item = params["item"]
        params["original_obtain_flag"] = location.original_obtain_flag if location.original_obtain_flag is not None else location.obtain_flag
        if item_id == item_table["Shell Horn"].game_code or item_id == item_table["Holy Grail (Full)"].game_code or item.obtain_flag is None:
            params["new_obtain_flag"] = self.filler_flags
            self.filler_flags += 1
        else:
            params["new_obtain_flag"] = item.obtain_flag

        if params.get("object_type") == RCD_OBJECTS["chest"]:
            params["obtain_value"] = 2
        else:
            params["obtain_value"] = item.obtain_value if item.obtain_value is not None else location.obtain_value
        self.local_config.add_item(params)
