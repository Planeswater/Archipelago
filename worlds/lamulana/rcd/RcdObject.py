from ..Rcd import Rcd
from ..LmFlags import RCD_OBJECTS


class RcdObject:

    def add_ops(self, test_ops, write_ops):
        self.rcd_object.test_operations = test_ops
        self.rcd_object.write_operations = write_ops

    def add_to_screen(self, rcd_mod, screen):
        if not hasattr(self.rcd_object, 'test_operations'):
            self.rcd_object.test_operations = []
        if not hasattr(self.rcd_object, 'write_operations'):
            self.rcd_object.write_operations = []

        self.rcd_object.test_operations_length = len(self.rcd_object.test_operations)
        self.rcd_object.write_operations_length = len(self.rcd_object.write_operations)
        self.rcd_object.parameters_length = len(self.rcd_object.parameters)

        if self.has_position():
            screen.objects_with_position.append(self.rcd_object)
            screen.objects_length += 1
        else:
            screen.objects_without_position.append(self.rcd_object)
            screen.objects_length += 1
            screen.objects_without_position_length += 1
    
        rcd_mod.file_size += self.obj_size() + self.ops_size() + self.params_size()

    def ops_size(self):
        return (self.rcd_object.test_operations_length + self.rcd_object.write_operations_length) * 4

    def params_size(self):
        return self.rcd_object.parameters_length * 2
