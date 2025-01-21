from .ObjectWithPosition import *


class InstantItem(ObjectWithPosition):

    def __init__(self, x, y, item, width, height, sound):
        super().__init__(x, y)
        self.rcd_object.id = RCD_OBJECTS["instant_item"]
        self.rcd_object.parameters = [item, width, height, sound]
