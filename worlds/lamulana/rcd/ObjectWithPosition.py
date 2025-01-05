from .RcdObject import *


class ObjectWithPosition(RcdObject):

    def __init__(self, x, y):
        self.rcd_object = Rcd.ObjectWithPosition()
        self.rcd_object.x_pos = x
        self.rcd_object.y_pos = y

    def obj_size(self):
        return 8

    def has_position(self):
        return True
