from .RcdObject import *


class ObjectWithoutPosition(RcdObject):

    def __init__(self):
        self.rcd_object = Rcd.ObjectWithoutPosition()

    def obj_size(self):
        return 4

    def has_position(self):
        return False
